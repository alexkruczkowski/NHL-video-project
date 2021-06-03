# NHL-video-project
An automated email recap of last night's NHL games with links to the game highlights. Built to still be able to catch the highlights when you don't have time to watch a game in the evening. 

## Contents

1. [Overview](#overview)
1. [The architecture](#the-architecture)
1. [Project demo](#project-demo)
1. [Built with](#built-with)
1. [Next steps](#next-steps)
1. [Author](#author)

## Overview

### What's the problem?
A hockey fan at heart, I love to watch NHL games when they are on TV. Unfortunately, most nights I find myself without the time to sit down and catch a full game. As a result, it is difficult to keep up with the games and going-on's in the league.

### The idea
Build an automated newsletter that sends last night's NHL scores and links to video recaps via email. Ideally build a no frills, hands off, and low cost solution.

### Bringing the idea to life
Initially the project will be split into three parts, with the potential addition of a fourth part afterwards. 
* Part 1: Build an ETL that fetches last night's results via the NHL API and uploads them to AWS S3 in CSV format
* Part 2: Create and schedule an automated email that reads the CSV file in S3. Use AWS ECR to upload the docker container to AWS and cron scheduling with ECS to run the email code in said docker container each morning
* Part 3: A REST API built on AWS using the serverless framework. Contains all subscribers to the recap newsletter and will be added to the process in part 2. 
* Part 4: Launch front end subscription and unsubscription pages for potential users 

## The architecture

### ETL
Retrieve last night's NHL games and video recaps via the [NHL API](https://statsapi.web.nhl.com/api/v1/configurations). 

Steps:
1. Retrieve yesterday's game data each morning. Pull scores, home & away teams, and links to NHL video recaps.  
1. Then completes a series of checks. Were any games played? Are there any null values? Are all the dates retrieved equal to yesterday's date? If all checks pass, move on to the next step. 
1. Publish a CSV file with the desired data to AWS S3 for use in the email process. This is an override of the previous day's data. 
 
Data considerations: Currently all old data is overwritten and lost. S3 bucket versioning could be enabled to retain history or a new file with the upload date in the file name could be added each day. If a new file is uploaded daily without deleting older data, an S3 lifecycle policy could be implemented to manage older files. 

A big thank you to Drew Hynes, who documented much of the NHL API and made it easier to find the data required. [Documentation can be found here](https://gitlab.com/dword4/nhlapi/-/tree/master).

### Automated Email
Send an automated email to the list of subscribers with yesterday's NHL scores and links to video recaps.

Methodology: read the CSV file from S3, format the contents using HTML, and send an email via AWS SES to the newsletter subscribers. 

Once code was working locally it was added to a docker container. That container was then published as an image and uploaded to AWS ECR. From there, an AWS ECS cluster was created with two tasks. One task for the ETL and a second for the automated email. Each task was then scheduled to run daily using a cron expression in ECS. 

Considerations: Currently SES requires all email addresses to be verified before emails can be sent to that address. In order to make this process smoother in the future, automate the AWS verification email so that it is sent before the next copy of the newsletter. 

### API
REST API containing a list of subscribers built using serverless architecture on AWS. 

Create the infrastructure as code using a SAM YAML template. API gateway for the API structure and endpoints, DynamoDB for storing the list of subscribers, and a lambda functions to tie it all together. This API will be leveraged as a part of the automated email process.

Next step: add the ability to subscribe / unsubscribe via a front end page. 

## Project demo

## Built with
* [Docker](https://www.docker.com/)
* [AWS ECR](https://aws.amazon.com/ecr/)
* [AWS ECS](https://aws.amazon.com/ecs/)
* [AWS S3](https://aws.amazon.com/s3/)
* [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
* [AWS API Gateway](https://aws.amazon.com/api-gateway/)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* [AWS DynamoDB](https://aws.amazon.com/dynamodb/)

## Next steps
With the ETL, API, and email process built and automated the next step is to build and deploy the front-end. You may notice that the process has already begun in the subscription page directory. The next step is to test post and delete requests to the API through the form in the HTML page. Once complete, the subscription page will be deployed using AWS services. 

## Author 
:wave:
Alex Kruczkowski
# putnam-mail
putnam-mail is a small Flask project I created to play around with API creation and consumption. My portfolio's contact form POSTs to the app, the app does more form validation such as ensuring there is a subject and valid email, and then POSTs to a transactional email service (Sendgrid).

Some of the endpoints for the app are weakly protected with authorization (flask-httpauth), weakly since the credentials could easily be found out by looking at the source tree of my portfolio website and looking at the form actions. As such, CORS is another layer of security by only allowing cross-origin requests from my portfolio website.

## Installation
```flask/bin/pip install -r requirements.txt```

## Deployment
Originally I wanted to have the project be deployable to either Zeit's Now platform (since it's free) or AWS. Unfortunately, Now does not have any good builders for Flask, so I'm stuck with AWS (or Heroku, or Dokku).

To deploy the project, you need the AWS Elastic Beanstalk CLI installed: ```pip install awsebcli```.

First you need to initialize a project on Elastic Beanstalk, the default options should be sufficient: ```eb init```.

Deploy with ```eb deploy```.

To actually use in production you would need to add SSL to the deployment, which you can do by verifying a domain name with AWS, creating an SSL certificate through AWS, and assigning the SSL cert to the load balancer.

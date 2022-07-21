<div id="top"></div>

<br />
<div align="center">

<h2 align="center">URL Shortener
</h2>
<p size=large> Final project of Cloud Computing course.</p>
<div align="center">
</div>
<br>
</div>

## Overview

A URL Shortener server with a MySQL database, containerized using Dockerfile and deployed on a Minikube cluster.

## Server
Developed using `flask`, given any URL creates the shortened form for it and stores that URL with it's short form in a MySQL database for a limited time. The server has been containerized using multi-stage build Dockerfile and uploaded to DockerHub. We use the `mysql:8.0.28` image for deployment of MySQL database.

## Deployment
Using `.yaml` files within `deployment` folder we are able to run this project on a `minikube` cluster, where we have a pod for our database with it's own claimed persistent volume and two replicated pods for our url-shortener server. Later we will use `db-statefullset.yaml` to deploy our database.  

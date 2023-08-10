## About The Project

The project involved developing a robust and secure blog application using Flask, HTML, CSS, Python, Bootstrap, and PostgreSQL. Key functionalities such as registration, login, post creation, and deletion were implemented, with thorough test cases ensuring quality.

The Infrastructure for the project was defined using terraform HCL.

To enhance development efficiency, a Continuous Integration and Continuous Deployment (CI/CD) pipeline was established. This pipeline automated the testing, building, and deployment of the web app to an ECS cluster. Docker Scout was integrated into the pipeline to scan the image for vulnerabilities before pushing it to the Elastic Container Registry (ECR). Additionally, old images were properly deleted to maintain a clean environment.

The application was deployed as a service utilizing two containers within the ECS cluster. One container hosted the web app, while the other container housed the PostgreSQL database. The web app container had a dependency on the PostgreSQL container, efficiently managed through health checks. This setup ensured seamless functionality of the blog application while maintaining security and scalability.

## Architecture

![Image](https://i.imgur.com/D0b8avi.png)

## Built With

* [![bootstrap][bootstrap.com]][bootstrap-url]
* [![Terraform][Terraform-logo]][Terraform-url]
* [![Python][Python-logo]][Python-url] 
* [![Docker][Docker-logo]][Docker-url] 
* [![GitLab][GitLab-logo]][GitLab-url] 
* [![AWS][AWS-logo]][AWS-url] 
* [![PostgreSQL][PostgreSQL-logo]][PostgreSQL-url] 
* [![HTML][HTML-logo]][HTML-url] 
* [![CSS][CSS-logo]][CSS-url] 
* [![Flask][Flask-logo]][Flask-url]

## Demo

To run the app. just download the docker-compose.yml, db.env and webapp.env

### Prerequisites

* docker
  ```sh
  https://docs.docker.com/get-docker
  ```
* docker-compose
  ```sh
  https://docs.docker.com/compose/install
  ```
  
### Getting Started

1. populate the .env files with the required credentials
2. pull and run the docker containers using docker-compose with
   ```sh
   docker-compose up
   ```
3. to stop the containers
   ```sh
   docker-compose down
   ```

### Clean up

#### docker image and container
   ```sh
      docker stop $(docker ps -q) && docker rm $(docker ps -aq) && docker rmi $(docker images -q)
   ```
#### docker volume
   ```sh
      docker volume rm $(docker volume ls -q)
   ```

## Screenshots

![Image](https://i.imgur.com/mw9bXqQ.png)
![Image](https://i.imgur.com/a0fi4Vl.png)
![Image](https://i.imgur.com/hICau9I.png)
![Image](https://i.imgur.com/d1C4omZ.png)
![Image](https://i.imgur.com/ffNOFXD.png)
![Image](https://i.imgur.com/ok0Qzmu.png)
![Image](https://i.imgur.com/eTpn7nP.png)





[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com

[Python-logo]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[Docker-logo]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/

[GitLab-logo]: https://img.shields.io/badge/GitLab-FCA121?style=for-the-badge&logo=gitlab&logoColor=white
[GitLab-url]: https://gitlab.com/

[AWS-logo]: https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white
[AWS-url]: https://aws.amazon.com/

[PostgreSQL-logo]: https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/

[HTML-logo]: https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML

[CSS-logo]: https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS

[Flask-logo]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.pocoo.org/

[Terraform-logo]: https://img.shields.io/badge/Terraform-623CE4?style=for-the-badge&logo=terraform&logoColor=white
[Terraform-url]: https://www.terraform.io/



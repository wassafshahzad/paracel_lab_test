## Running theApplication using Docker
Make sure you have docker and docker-compose installed. This application is dependent on postgres and redis and used docker containers to quaickly spin them up.

### Running the application intructions.
 - Start docker engine if its not already running.
 - Open a terminal in the parcel_lab_test folder.
 - Run **docker-compose build** and **docker-compose up**
 - Once the web service is up and running visit **localhost:8000** for the swagger docs and test the application out

### Running Tests
- Make sure the web service is running.
- Attach to the web service using the command **docker-compose exec web bash**
- Run the command **Python manage.py tests**

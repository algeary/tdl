
   To run a local version of the code, run the following commands from your terminal:
      python -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
      docker run -p 8080:8080 -e hapi.fhir.default_encoding=xml hapiproject/hapi:latest

   Once the server started by the previous docker command has finished initializing, you can run the following commands:
      export SECRET_KEY="fakesecret123"
      If you want to send email reminders from your email, set local environment variables named EMAIL_ADDRESS and EMAIL_PASS.
      python manage.py makemigrations
      python manage.py migrate
      python manage.py createsuperuser
      python manage.py runserver
   Now, you can access the application in your web browser at http://127.0.0.1:8000/. You can create your own account, or view an existing dummy account with the following credentials: allisongeary, pandaCall25$

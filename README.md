# urlpdfmailer
A simple Dockerised Python script that emails a PDF version of a URL on a schedule. This is a classic sticky tape
solution to a problem much better solved by a web developer but we don't all have that luxury!

## Example config file
The script can be configured simply with a `yaml` file like the following:

```yaml
sites:
  - login_url: https://www.mysite.co.uk/login
    verify: my-custom-ssl-verification.pem
    login_form_id: new_user
    username: my@email.co.uk
    password: my_very_secure_password_123
    username_field_id: username
    password_field_id: password
    pages_to_export:
        output_file_1: https://www.mysite.co.uk/this_page
        output_file_2: https://www.mysite.co.uk/and_also_this_one
    email:
      to: my@friend.co.uk
      bcc: my@email.co.uk
      subject: Here's some things!
      body: I've attached some print-outs from my website, check it out!
ssl_email_settings:
  email_address: my@email.co.uk
  password: my_VERY_secure_PASSWORD_1234
  host: smtp.gmail.com
  port: 465
```

## Running the service
This repo is configured with Docker-compose so provided that the config file is valid, running `docker-compose up` 
will start the service.
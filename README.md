#Item Catalog

This is the fourth project for the Udacity Full Stack Nanodegree. 
The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system. 
This project uses persistent data storage to create a RESTful web application that allows users to perform Create, Read, Update, and Delete operations.

PreRequisites:
Python 2.7
Vagrant
VirtualBox
Setup Project:

Set up:
Vagrant
Udacity Vagrantfile
VirtualBox

Getting Started:
Install Vagrant and VirtualBox
Clone the Vagrantfile from the Udacity Repo
Clone this repo into the catlog/ directory found in the Vagrant directory
Run vagrant up to run the virtual machine, then vagrant ssh to login to the VM
Run database_setup.py to create the database
Run populate_db to populate the database
Run application with python application.py from within its directory
Go to http://localhost:8000/ to access the application

#JSON ENDPOIT
 http://localhost:8000/category/Soccer/json'
 {
  "Items": [
    {
      "category_id": 1, 
      "category_name": "Soccer", 
      "description": "The most famousteam in northeast", 
      "id": 1, 
      "name": "Ceara"
    }, 
    {
      "category_id": 1, 
      "category_name": "Soccer", 
      "description": "The rival of most famous team in northeast", 
      "id": 2, 
      "name": "Fortaleza"
    }
  ]
}


# Image tagging:
API endpoints to manage images and the corresponding tags

# Project description(provided):
Annalise.ai is designing an image tagging system that will help add tags to images that will be used
for training a model. You are to create an API to manage images and their tags. Your API needs to
support the ability to persist and modify data.

# Prerequisites:
* Anaconda - use the below command to create the environment
  * ```conda env create -f docs/conda_environment.yml```
* MySQL server - to persist data - use the below command to create the initial data (user has to be created separately)
  * ```services/image/models/schema/document_management_schema.sql```
  * ```services/image/models/schema/document_management_initial_data.sql```
* Python3.7
* Postman or similar application

# Steps to run:
* Run the `main.py` file to invoke the flask application
* Post request from postman to get the required details. Use `image_tagging/docs/postman_collection/image_management.postman_collection.json` for sample request response format

# Unit test and coverage:
Unit test cases are located in `image_tagging/tests` folder. Use Pycharm or command line to execute the test cases and coverage.

# Additional information requested
* What would your ideal environment look like and how does this fit into it?
  * This service should be containerized which can then be deployed using a web server
* How are subsequent deployments made?
  * As of now, it has to be deployed again whenever code changes are made after ensuring quality
* How could you avoid downtime during deployments?
  * We could use rolling deployment which will make the deployment process smoother as requests would be still server using stable code unless the new services are up and running fine
* Assuming a stateless application, what does immutable infrastructure look like?
  * Terraform or cloudformation code?
* What was missed in this implementation?
  * Added very few test cases and lots of enhancements need to be done such as containerization, separate config files for various environments, sha2 password hashing instead of plain text storage and many more optimizations
* What would you have liked to have added?
  * could have increased the code coverage 
  * could have added results of static code analysers
  * open api documentation
  * containerization
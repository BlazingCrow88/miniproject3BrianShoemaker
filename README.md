# Recipe Sharing Platform - Flask Web Application

## Project Overview

The Recipe Sharing Platform is a comprehensive web application built using Flask that enables users to create, share, and discover recipes from a community of food enthusiasts. This application demonstrates modern web development practices, including user authentication, database relationships, form handling, and responsive design using Bootstrap.

The platform provides a complete user experience where members can register for an account, log in securely, create their own recipe collections, and browse recipes shared by other community members. Each recipe includes detailed information such as ingredients, step-by-step instructions, preparation and cooking times, serving sizes, and categorization to help users find exactly what they need.

## Technical Features

This application has been designed to meet comprehensive educational requirements while demonstrating industry best practices. The system implements a proper Model-View-Controller architecture with SQLAlchemy for database management. User authentication is handled securely using Werkzeug's password hashing utilities to ensure that sensitive credential information is protected.

The database architecture consists of two primary tables linked through a foreign key relationship. The Users table stores authentication credentials and user profile information, while the Recipes table maintains recipe content with a foreign key reference to the author. This establishes a one-to-many relationship where each user can create multiple recipes, and each recipe belongs to exactly one user.

The application includes seven distinct pages that provide complete functionality for the recipe sharing experience. These pages include the home page, registration page, login page, all recipes browsing page, individual recipe detail page, recipe creation form, and user profile page. The templating system uses Jinja2 with a base template that all other pages extend, ensuring consistent navigation, styling, and structure throughout the application.

Bootstrap 5 has been integrated throughout the application to provide a modern, responsive user interface that works seamlessly across desktop and mobile devices. The implementation includes various Bootstrap components such as cards, forms, buttons, navigation bars, and modals. The modal component is specifically utilized for delete confirmation dialogs to prevent accidental data loss.

## Installation Instructions

To set up this application on your local development environment, you will need to ensure that Python 3.8 or higher is installed on your system. The installation process involves several steps that must be completed in sequence to prepare the application for execution.

Begin by cloning or downloading this repository to your local machine. Once you have obtained the project files, navigate to the project root directory using your terminal or command prompt. This directory should contain the app.py file along with the templates folder and other project components.

The next step involves creating a Python virtual environment, which is a best practice for managing project dependencies in isolation from your system Python installation. You can create a virtual environment by executing the command `python -m venv venv` on Windows systems or `python3 -m venv venv` on macOS and Linux systems. This command will create a new directory called venv within your project folder that contains the isolated Python environment.

After creating the virtual environment, you must activate it before proceeding. On Windows, activation is accomplished by running `venv\Scripts\activate`. For macOS and Linux users, the activation command is `source venv/bin/activate`. When the virtual environment is successfully activated, you will typically see the environment name appear in your terminal prompt, indicating that you are now working within the isolated environment.

With the virtual environment activated, you can install all required dependencies by executing `pip install -r requirements.txt`. This command reads the requirements.txt file and installs all necessary Python packages including Flask, SQLAlchemy, and their dependencies. The installation process may take a few moments to complete as pip downloads and configures each package.

## Database Initialization

Before running the application for the first time, the database must be properly initialized. The application uses SQLite as its database engine, which stores all data in a single file. The database initialization process creates the necessary tables and establishes the relationships between them according to the models defined in the application.

The database file will be automatically created when you first run the application, as the code includes logic to detect whether the database exists and creates it if necessary. However, if you prefer to initialize the database manually or need to reset it, you can use Python's interactive shell to execute the initialization commands directly.

To manually initialize the database, ensure your virtual environment is activated and execute `python` to start the Python interactive shell. Within the shell, import the necessary components by running `from app import app, db`. Next, create an application context with `app.app_context().push()`, which sets up the Flask application environment required for database operations. Finally, execute `db.create_all()` to create all database tables according to your models. You can then exit the Python shell by typing `exit()`.

If you need to reset the database at any point during development or testing, you can delete the database file located at `instance/recipes.db` and then repeat the initialization process. This will create a fresh database with empty tables, allowing you to start with a clean slate.

## Running the Application

Once the installation and database initialization steps are complete, you are ready to run the application. Ensure that your virtual environment remains activated throughout the execution of the application. To start the Flask development server, execute the command `python app.py` from the project root directory.

The development server will initialize and begin listening for HTTP requests. By default, Flask runs on port 5000 of your local machine. Once the server has started successfully, you will see output in your terminal indicating that the application is running. You can access the application by opening your web browser and navigating to `http://localhost:5000` or `http://127.0.0.1:5000`.

The development server includes debug mode, which provides several useful features during development. When debug mode is enabled, the server automatically reloads when you make changes to the code, allowing you to see your modifications immediately without manually restarting the server. Additionally, if an error occurs, Flask will display a detailed error page in the browser with stack traces and debugging information to help identify and resolve issues.

It is important to note that the development server is intended only for development and testing purposes. It should never be used in a production environment as it is not designed to handle high traffic loads or provide the security features necessary for public-facing applications. For production deployment, you would need to use a proper WSGI server such as Gunicorn or uWSGI behind a reverse proxy like Nginx.

## Using the Application

Upon first accessing the application, you will be presented with the home page which showcases recently added recipes and provides options to register for an account or browse the recipe collection. New users should click the Register button to create an account, which requires providing a unique username, email address, and secure password.

After successful registration, you will be redirected to the login page where you can authenticate using your newly created credentials. Once logged in, you gain access to additional features including the ability to create and manage your own recipes. The navigation bar updates to reflect your authenticated status and provides quick access to your profile and recipe management functions.

To create a new recipe, click the Add Recipe link in the navigation menu. You will be presented with a comprehensive form that captures all aspects of your recipe including the title, description, ingredients list, cooking instructions, preparation and cooking times, serving size, and category. All required fields are clearly marked and must be completed before the recipe can be submitted.

After submitting a recipe, it becomes immediately available in the recipe collection where other users can discover and view it. Each recipe displays the author information, timing details, and serving information in an easy-to-read format. Users can click on any recipe to view its complete details including the full ingredient list and step-by-step instructions.

Your profile page provides a centralized location to manage all recipes you have created. From this page, you can view your complete recipe collection, edit existing recipes to update their information, or delete recipes that you no longer wish to share. The edit functionality preserves your existing recipe data and allows you to modify any field before saving the updates.

## Project Structure

The application follows Flask best practices for project organization with a clear separation of concerns. The main application logic resides in app.py, which contains all route definitions, database models, and application configuration. The templates directory houses all HTML template files that use Jinja2 syntax for dynamic content rendering.

Within the templates directory, the base.html file serves as the master template that defines the common structure shared across all pages including the navigation bar, footer, and Bootstrap integration. All other template files extend this base template to maintain consistent styling and functionality. The static directory, if created, would contain CSS stylesheets, JavaScript files, and images, though this basic implementation primarily relies on Bootstrap's CDN for styling.

Database files are stored in the instance directory, which Flask creates automatically. This directory is typically excluded from version control as it contains data specific to each deployment. The instance directory provides a standardized location for database files and other instance-specific configuration that should not be shared across different deployments of the application.

## Development Notes

This project has been structured to demonstrate comprehensive Flask development skills including user authentication with password hashing, database relationships with foreign keys, form handling with both GET and POST methods, template inheritance, and Bootstrap integration. The codebase includes extensive comments explaining the purpose and functionality of each component to facilitate learning and future maintenance.

The application implements proper security practices including password hashing using Werkzeug's security utilities, session management for maintaining user authentication state, and access control decorators to protect routes that require authentication. The database schema has been designed with appropriate relationships and constraints to maintain data integrity.

Commit history should reflect incremental development with clear, descriptive commit messages documenting each feature addition or modification. Regular commits throughout the development process provide a detailed record of the project's evolution and make it easier to identify when specific features were implemented or bugs were introduced.

## Troubleshooting

If you encounter issues during installation or execution, several common problems have straightforward solutions. Import errors typically indicate that the virtual environment is not activated or that dependencies were not installed correctly. Ensure that your virtual environment is activated and try reinstalling the requirements using `pip install -r requirements.txt`.

Database errors often stem from the database not being properly initialized or from attempting to access tables before they have been created. Delete the instance/recipes.db file and restart the application to trigger automatic database creation, or manually initialize the database using the Python shell as described in the Database Initialization section.

Port conflict errors occur when another application is already using port 5000. You can either stop the conflicting application or modify app.py to use a different port by changing the port parameter in the app.run() call. Authentication issues where users cannot log in despite having registered successfully may indicate problems with password hashing and should be investigated by reviewing the User model's password methods.

## Future Enhancements

While this application provides comprehensive core functionality, several enhancements could further improve the user experience and demonstrate additional technical capabilities. Potential additions include recipe search functionality to help users find specific recipes quickly, a rating and review system to allow community feedback on recipes, image upload capabilities to make recipes more visually appealing, user-to-user messaging for sharing cooking tips, and advanced filtering options for dietary restrictions or ingredient availability.

Additional technical improvements could include implementing email verification during registration, adding password reset functionality, implementing proper logging for debugging and monitoring, creating an administrative interface for content moderation, and optimizing database queries for improved performance as the recipe collection grows.

## License and Credits

This project was created as an educational assignment to demonstrate Flask web development skills. The application showcases fundamental concepts including database design, user authentication, form handling, and modern web design using Bootstrap. All code has been written with attention to best practices and includes comprehensive comments for educational purposes.

## Contact Information

For questions, issues, or suggestions regarding this project, please refer to the repository's issue tracker or contact the project maintainer. Contributions and feedback are welcome as this project serves as both a learning tool and a functional application that can be extended with additional features.
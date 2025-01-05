# LittleLemon API

LittleLemon API is a Django-based web application designed to manage and serve data for the LittleLemon application.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed Python 3.10 or later.
- You have installed `pip` (Python package installer).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/amp-bay/LittleLemon.git
    cd LittleLemon
    ```

2. Install `pipenv`:
    ```bash
    pip3 install pipenv
    ```

3. Create and activate a virtual environment:
    ```bash
    pipenv --python 3.10
    pipenv shell
    ```

4. Install project dependencies:
    ```bash
    pipenv install
    ```

## Running the Application

1. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

2. Start the development server:
    ```bash
    python manage.py runserver
    ```

3. Open your browser and navigate to `http://127.0.0.1:8000` to see the application running.

## Testing

To run tests, use the following command:
```bash
python manage.py test
```

## Additional Information

The `notes.txt` file contained in the `LittleLemonApiApp` directory has the login details and token requirements:
- `af25943c7300cec9b29100090b7fc880058e28c4` Adebayoo-MANGER
- `4250e2d0115475c75cf894de913c7a9aca0b5f6b` Emeka-DELIVERY
- `154760173b6e1b5adb13000b118afc16f6b95a61` admin
- `62eac7c8ab558591704f22ee7938e7b8c2383270` Sam-Customer
- Username: `admin`, Password: `admin123456789`

## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit the changes (`git commit -m 'Add feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a pull request.


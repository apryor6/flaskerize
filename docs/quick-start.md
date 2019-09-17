# Flaskerize Quick-Start Tutorial

This guide is designed to get you up and running by showing you how to create a new Flask API using Flaskerize. We'll perform the following steps in this quick-start...

1. Create a new folder and set up a virtual environment
2. Install Flaskerize
3. Use Flaskerize to create an initial Flask API
4. Use Flaskerize to add an entity to your API

## Pre-Requisites and Assumptions

It's assumed that you have Python 3.7 installed. The illustrations in this tutorial assume that you're using a bash terminal, and that you're comfortable using a command line.

OK....let's start...

## Step 1 - Create a New Folder and Set Up a Virtual Environment

Let's assume you're started from nothing. First, let's create a folder for your Flask API to live in.

```bash
mkdir flaskerize-example
cd flaskertize-example
```

Now, let's set up a virtual environment for our API project, activate it, and then upgrade `pip` within that environment.

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

## Step 2 - Install Flaskerize

We're now ready to install Flaskeriez. Let's use `pip` to do just that...

```bash
pip install --upgrade pip
```

Once this command has completed you will have installed Flaskerize along with its dependencies. If you want to see the packages that were installed, run the following command:

```bash
pip list
```

This should show you something like this...

``` bash
$ pip list
Package      Version
------------ -------
appdirs      1.4.3
Click        7.0
Flask        1.1.1
flaskerize   0.10.0
fs           2.4.11
itsdangerous 1.1.0
Jinja2       2.10.1
MarkupSafe   1.1.1
pip          19.2.3
pytz         2019.2
setuptools   40.8.0
six          1.12.0
termcolor    1.1.0
Werkzeug     0.15.6
```

> note: the exact version numbers shown here may differ
>
## Step 3 - Use Flaskerize to create an initial Flask API

You're now ready to create your Flask API.

```bash
fz generate app myapi
```

```bash
fz generate setup myapi
```

## Step 4 - Use Flaskerize to add an entity to your API

```bash
fz generate entity cake
```

# Follow the following steps to set up your enviourement and start to contribute.

### 1, Make sure you have all nessecary softwares installed.

Install the following softwares and dependecies before starting.

* python 3.7 [install](https://www.python.org/)
* git

## 2, Install necessary dependecies.

* upgrade your python package manager pip

    ```bash
    python -m pip install --upgrade pip
    ```

* install pipenv for package control.

    ```bash
    pip install pipenv
    ```

## 2, Fork this project to your own GitHub account.

## 3, Clone to your local enviourment.

```
git clone https://github.com/endalk200/CodeTopia.git
```

## 4. Update your master branch.

Keeping your master branch is verry crucial since there may be some changes made after forking the repo. You should regulary update your master branch. To dod this run the following command.

```bash
git add upstream https://github.com/endalk200/CodeTopia.git

git fetch upstream 

git branch --set-upstream-to=upstream/master master 

git pull
```

## 5. Create virtualenv using pipenv.

run this command to install all dependencies.

```bash
pipenv install
```

## 6, Run tests

```bash
flake8
python manage.py test
```

## 6, Create a branch to work on.

Create a branch and work on your idea. To do this run.

```bash
git checkout -b <branch name>
```

## You can also use docker whcih makes it easier to set up your envirounment
* install docker
* run:
```bash
docker-compose build
```
```bash
docker-compose up
```

Done! your ready to go.
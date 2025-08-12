# Set up

In order to connect to Judilibre, you need to have an active [PISTE](https://piste.gouv.fr) account.

> We will not cover how to use the sandbox, uniquely the PRODUCTION environment. 

## Creating an account

First, you need to create an account by going to the [registration menu](https://piste.gouv.fr/en/registration).

You will need to provide:
- your full name
- your email address
- a password
- accepts the Terms and Conditions of PISTE

Once this is done, you will receive an email with a link to validate your account.
For your first connection, you will be prompted with the terms and conditions to accept once again.

## Terms of Service Acceptance

PISTE is a platform that serves mutliple APIs from the French administrations. You need to accept the Terms of Service of every API you want to use.

Go to [APIS > APIS ToS Acceptance](https://piste.gouv.fr/en/apimgt/api-tos) and check `JUDILIBRE` for both `PROD` and `SANDBOX` environments. You can then click on `Confirm my ToS choices`.

## Creating an application

In order to use JUDILIBRE, you will need to create an application. To do so, you can click on [Applications](https://piste.gouv.fr/en/apps) and then click on `Create an application`.

You need to give an `Application name`. For the other fields, you can put any value. 


## Modifying the application

Once the application is created, you can click on it in the [Applications](https://piste.gouv.fr/en/apps) tab.
You can then `Edit this application`. In the table at the bottom of the page, select `JUDILIBRE` and `Apply changes`.

## Accessing your key

To use pyJudilibre, you need to use an API Key. This key is available in the main tab of the application table under `API Key`.
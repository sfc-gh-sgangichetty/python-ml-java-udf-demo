This demo shows how you can use a pure python ML workflow to build a model and then push the model into snowflake as a Java UDF for deployment. You can use this to demonstrate

1. The dockerfile on this repo builds on [snowtire](https://github.com/zoharsan/snowtire_v2). Therefore you need snowtire image. Clone the repo & build snowtire docker image as  `docker build --pull -t snowtire .` This will take a couple of minutes.

2. After this run `docker build -t citibike-pyjavaudf-v1:latest .` 

3. Once #3 is done, you can simply launch jupyterlab for the demo using `docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan/work citibike-pyjavaudf-v1:latest`

4.  Key Pair authentication (optional): 
    - Should you choose to do this, generate a keypair and register it on snowflake as shown in the docs [here](https://docs.snowflake.com/en/user-guide/key-pair-auth.html#configuring-key-pair-authentication). 
    - Move your private key to `my_pk` folder. There's a placeholder file on this folder. You can delete it or leave it as is. 
    - Update the following settings on the `src/pkb_auth.py` file: `PRIVATE_KEY_PASSPHRASE`, `<path-to-your-private-key>` and `account_id` variable. Follow the comments on the script to accomplish this. 

5. If you choose not to do #4, establish connection to snowfalke using the usual username/password based authentication.


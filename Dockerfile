# Start from snowtire
FROM snowtire:latest
# Install FB Prophet
# SEE https://github.com/facebook/prophet/issues/401 issue below. Pystan < 3 needs to be installed first
# RUN pip install pystan==2.18
# RUN python -m pip install fbprophet
RUN python -m pip install --user --force-reinstall --upgrade snowflake-connector-python[pandas]
RUN python -m pip install xgboost
RUN python -m pip install m2cgen
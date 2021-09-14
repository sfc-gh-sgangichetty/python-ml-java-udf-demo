import pandas as pd
def score_new_data(f_date, base_tbl,dates_tbl,results_tbl,start_station='Pershing Square North') -> str:
    """
    Constructs Queries based on Args Passed
    Makes Some Assumptions on start_station  and results_tbl.
    Pass other objects if need to change
    """
    score_min_transaction = f"""
    insert into {results_tbl}
    select *,
    score_xgbmodel(
    array_construct( 
    YEAR,MONTH_NUM,
    DOM,
    DAY_OF_WEEK_NUM,
    WEEK_NUM,
    QUARTER_NUM,
    LY_VAL,
    LAST_YEAR_DOW,
    LE_START_STATION,
    LAG_1_VAL,
    LAG_2_VAL,
    LAG_7_VAL)
    ) as model_prediction
    from {base_tbl} where DS='{f_date}' and start_station='{start_station}';
    """
    score_cte_sql =f"""
    insert into {results_tbl}
    with prep_data as
    (
    select 
    a.DS, a.start_station,
    results.next_prediction as trips,// always comes from results
    year(a.ds) as year, 
    month(a.ds) as month_num,
    dayofmonth(a.ds) as dom,
    dayofweek(a.ds) as day_of_week_num,
    weekofyear(a.ds) as week_num,
    quarter(a.ds) as quarter_num,
    b.ds as last_year_date,
    b.trips as ly_val,
    dayofweek(b.ds) as last_year_dow,
    c.le_start_station,
    c.trips as lag_1_val,
    c.lag_1_val as lag_2_val,
    d.trips as lag_7_val,
    null as next_trips
    from prediction_dates a 
    inner join {base_tbl} b on  DATEADD(YEAR, -1, a.ds) = b.ds and a.start_station=b.start_station
    inner join (select * from {results_tbl} where ds='{f_date - pd.Timedelta(1,'D')}')c on c.start_station = b.start_station
    inner join {base_tbl} d on  DATEADD(day, -8, a.ds) = d.ds and a.start_station=d.start_station
    inner join (select * from {results_tbl} where ds='{f_date - pd.Timedelta(1,'D')}')results on results.start_station = a.start_station
    where a.ds = '{f_date}'
     )
     select prep_data.*,
    score_xgbmodel(
    array_construct( 
    prep_data.YEAR,
    prep_data.MONTH_NUM,
    prep_data.DOM,
    prep_data.DAY_OF_WEEK_NUM,
    prep_data.WEEK_NUM,
    prep_data.QUARTER_NUM,
    prep_data.LY_VAL,
    prep_data.LAST_YEAR_DOW,
    prep_data.LE_START_STATION,
    prep_data.LAG_1_VAL,
    prep_data.LAG_2_VAL,
    prep_data.LAG_7_VAL)
    ) as next_prediction from prep_data;"""
    return score_min_transaction, score_cte_sql
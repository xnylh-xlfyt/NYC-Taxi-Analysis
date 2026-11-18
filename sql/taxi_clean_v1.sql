CREATE OR REPLACE VIEW yellow_taxi_clean_v1 AS
WITH BASE1 AS(SELECT
    *,
    CASE
        WHEN trip_distance>0 AND trip_distance<=1000
        THEN trip_distance
        ELSE NULL
    END AS clean_trip_distance,
    CASE WHEN trip_distance IS NULL THEN 'missing'
    WHEN trip_distance < 0 THEN 'negative'
    WHEN trip_distance = 0 THEN 'zero'
    WHEN trip_distance > 0  AND trip_distance <= 1000 THEN 'valid'
    ELSE 'above_limit'
    END AS distance_status
FROM yellow_taxi_data
),
BASE2 AS(
    SELECT *,
            EXTRACT(EPOCH FROM tpep_dropoff_datetime - tpep_pickup_datetime)/60 AS raw_duration_min
    FROM BASE1
)
SELECT *,
        CASE WHEN raw_duration_min > 0 AND raw_duration_min <= 600 THEN raw_duration_min
        ELSE NULL END AS clean_duration_min,

        CASE WHEN raw_duration_min IS NULL THEN 'missing'
        WHEN raw_duration_min =0 THEN 'zero'
        WHEN raw_duration_min <0 THEN 'negative'
        WHEN raw_duration_min >0 AND raw_duration_min <=600 THEN 'valid'
        ELSE 'above_limit' END AS duration_status,

        CASE WHEN fare_amount IS NULL or total_amount IS NULL THEN 'missing'
        WHEN fare_amount<0 or total_amount<0 THEN 'negative_present'
        ELSE 'non_negative' END AS amount_status

FROM BASE2;
SELECT *
FROM INPUT_SENSORS
WHERE timeStamp BETWEEN :startDate AND :endDate AND greenHouseId = :greenHouseId

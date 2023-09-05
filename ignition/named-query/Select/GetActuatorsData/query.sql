SELECT *
FROM OUTPUT_ACTUATORS
WHERE timeStamp BETWEEN :startDate AND :endDate AND greenHouseId = :greenHouseId

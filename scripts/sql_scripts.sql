-- Поиск медианы для задания порогового значения - 52,000
SELECT
 PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "Стоимость программы") AS median_cost
FROM Программы;

-- Поиск медианы слушателей на программах - 13
SELECT 
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "Численность слушателей накопленным итогом") AS median_listeners
FROM Программы;

-- Создание представления таблицы в БД 
CREATE OR REPLACE VIEW contingent_polygons AS
SELECT 
    g."region" AS region,
    COUNT(c."region") AS cnt_listeners,
    g."geometry" AS geometry
FROM "regions_geojson" g
LEFT JOIN "КонтингентРегион" c
    ON g."region" = c."region"
GROUP BY g."region", g."geometry"
ORDER BY g."region";

-- SQL Lab script to add geojson table
SELECT 
  g."region" AS region,
  COUNT(c."region") AS cnt_listeners,
  g."geometry" AS geometry
FROM "regions_geojson" g
LEFT JOIN "КонтингентРегион" c
  ON TRIM(g."region") = TRIM(c."region")  -- или regexp_replace(...)
GROUP BY g."region", g."geometry"
ORDER BY g."region";

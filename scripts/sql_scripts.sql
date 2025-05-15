-- Поиск медианы для задания порогового значения - 52,000
SELECT
 PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "Стоимость программы") AS median_cost
FROM Программы;

-- Поиск медианы слушателей на программах - 13
SELECT 
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "Численность слушателей накопленным итогом") AS median_listeners
FROM Программы;


SELECT 
  "Кампус НИУ ВШЭ, на базе которого реализуется программа" AS campus,
  "Уровень программы" AS program_level,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "Стоимость программы") AS med_cost,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "Численность слушателей накопленным итогом") AS med_listeners
FROM Программы
GROUP BY 
  "Кампус НИУ ВШЭ, на базе которого реализуется программа",
  "Уровень программы";

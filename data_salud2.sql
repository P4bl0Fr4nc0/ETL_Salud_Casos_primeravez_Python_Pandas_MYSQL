Use casos_primera_vez;

Select * FROM casos_nuevos;


SELECT 
    Diagnostico AS Casos_Mama,
    COUNT(*) AS total_casos
FROM casos_nuevos
WHERE Diagnostico LIKE 'C50%'
GROUP BY Diagnostico
ORDER BY total_casos DESC;
import pandas as pd
import io
import re

def get_truth_data():
    """
    Contiene y devuelve los datos definitivos proporcionados por el usuario.
    Esta es la ÚNICA fuente de la verdad.
    """
    
    # Los datos exactos proporcionados por el usuario.
    raw_data = """1996Amazonas3163.3
1997Amazonas3152.93
1998Amazonas3143.98
1999Amazonas3140.61
2000Amazonas3134.03
2001Amazonas3124.7
2002Amazonas3118.9
2003Amazonas3119.73
2004Amazonas3114.62
2005Amazonas3113.58
2006Amazonas3111.63
2007Amazonas3109.34
2008Amazonas3111.3
2009Amazonas3104.58
2010Amazonas3102.77
2011Amazonas3108.66
2012Amazonas3113.44
2013Amazonas3113.39
2014Amazonas3113.11
2015Amazonas3110.98
2016Amazonas3110.27
2017Amazonas3104.47
2018Amazonas3098.3
2019Amazonas3098.52
2020Amazonas3094.26
2021Amazonas3085.27
2022Amazonas3076.7
2023Amazonas3061.32
1996Loreto34979.15
1997Loreto34965.51
1998Loreto34942.16
1999Loreto34909.67
2000Loreto34903.73
2001Loreto34898.35
2002Loreto34906.56
2003Loreto34915.69
2004Loreto34910.25
2005Loreto34879.84
2006Loreto34875.82
2007Loreto34879.63
2008Loreto34858.02
2009Loreto34847.02
2010Loreto34817.58
2011Loreto34790.33
2012Loreto34742.91
2013Loreto34710.39
2014Loreto34676.31
2015Loreto34637.31
2016Loreto34639.79
2017Loreto34609.01
2018Loreto34633.22
2019Loreto34610.29
2020Loreto34563.61
2021Loreto34516.29
2022Loreto34425.03
2023Loreto34365.64
1996Madre de Dios8203.52
1997Madre de Dios8200.57
1998Madre de Dios8197.98
1999Madre de Dios8194.47
2000Madre de Dios8192.02
2001Madre de Dios8179.91
2002Madre de Dios8177.64
2003Madre de Dios8171.06
2004Madre de Dios8167.44
2005Madre de Dios8166.54
2006Madre de Dios8162.28
2007Madre de Dios8153.47
2008Madre de Dios8142.4
2009Madre de Dios8136.55
2010Madre de Dios8129.54
2011Madre de Dios8125.11
2012Madre de Dios8117.72
2013Madre de Dios8110.4
2014Madre de Dios8089.81
2015Madre de Dios8077.84
2016Madre de Dios8067.12
2017Madre de Dios8052.53
2018Madre de Dios8045.91
2019Madre de Dios8024.63
2020Madre de Dios8025.92
2021Madre de Dios8014.21
2022Madre de Dios7986.43
2023Madre de Dios7967.1
1996San Martin3951.9
1997San Martin3935.25
1998San Martin3916.64
1999San Martin3902.73
2000San Martin3889.71
2001San Martin3871.8
2002San Martin3858.57
2003San Martin3839.09
2004San Martin3825.05
2005San Martin3804.14
2006San Martin3785.17
2007San Martin3764.83
2008San Martin3749.49
2009San Martin3732.19
2010San Martin3714.47
2011San Martin3706.49
2012San Martin3693.58
2013San Martin3690.01
2014San Martin3691.67
2015San Martin3686.85
2016San Martin3681.68
2017San Martin3682.88
2018San Martin3684.95
2019San Martin3700.02
2020San Martin3686.04
2021San Martin3661.71
2022San Martin3642.02
2023San Martin3622.45
1996Ucayali9805.02
1997Ucayali9804.73
1998Ucayali9799.48
1999Ucayali9799.23
2000Ucayali9796.29
2001Ucayali9794.13
2002Ucayali9791.26
2003Ucayali9783.31
2004Ucayali9782.24
2005Ucayali9772.53
2006Ucayali9763.2
2007Ucayali9756.83
2008Ucayali9754.28
2009Ucayali9736.3
2010Ucayali9717.04
2011Ucayali9704.9
2012Ucayali9691.45
2013Ucayali9667.62
2014Ucayali9653.85
2015Ucayali9634.52
2016Ucayali9618.68
2017Ucayali9592.47
2018Ucayali9576.76
2019Ucayali9542
2020Ucayali9505.34
2021Ucayali9457.83
2022Ucayali9395
2023Ucayali9354.71
"""
    
    # Parser robusto para el formato de texto proporcionado.
    lines = raw_data.strip().split('\n')
    data = []
    # Regex: Captura año (4 digitos), nombre de departamento (letras y espacios), y cobertura (número al final)
    pattern = re.compile(r"(\d{4})([A-Za-z\s]+)(\d+\.?\d*)")

    for line in lines:
        match = pattern.match(line)
        if match:
            periodo, departamento, cobertura = match.groups()
            data.append([int(periodo), departamento.strip(), float(cobertura)])

    df = pd.DataFrame(data, columns=['Periodo', 'departamento', 'cobertura_boscosa'])
    
    # Recalcular 'deforestacion_anual'
    # Se ordena por departamento y periodo para asegurar que el .diff() sea correcto.
    df = df.sort_values(by=['departamento', 'Periodo']).reset_index(drop=True)
    df['deforestacion_anual'] = df.groupby('departamento')['cobertura_boscosa'].diff().mul(-1)
    
    return df

def save_processed_data(df, path, logger):
    """
    Guarda el DataFrame en la ruta especificada y registra el resultado.
    """
    try:
        # Asegurarse de que el directorio de salida exista
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False, float_format='%.2f')
        logger.info(f"Datos guardados exitosamente en '{path}'")
        return True
    except Exception as e:
        logger.error(f"FALLO al guardar los datos en '{path}'. Error: {e}")
        return False
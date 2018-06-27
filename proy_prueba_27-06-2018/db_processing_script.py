import module_dbreader as dbr
import settings as st

def processing(fileName):
    
    ######################################################
    
    
    #Abrir libro Excel y obtener las hojas de cálculo...            
    xl_sheet = dbr.F_get_xl_sheets(fileName)
    ######################################################
    
    
    #Rescatar las matrices con la información de las Semanas, las Prácticas y de las
    #Actividades desde Excel...
    DATA_matrix_Weeks = dbr.F_translate_into_week(xl_sheet).week_L
    DATA_matrix_Pract = dbr.F_translate_into_week(xl_sheet).pract_L
    DATA_matrix_Act = dbr.F_translate_into_week(xl_sheet).act_L
    DATA_matrix_Cent = dbr.F_translate_into_week(xl_sheet).cent_L
    DATA_list_Lin = dbr.F_translate_into_week(xl_sheet).lin_L
    
    ######################################################
    
    
    #Rescatar matriz de profesores...
    DATA_matrix_Prof = dbr.F_get_prof_data(xl_sheet['Profesores'])
    ######################################################
    
    #Crear parámetro e_p_k (match entre especialidades profesor-actividad)...
    #PARAM_ematch_PA = ini.F_ematch_prof_act(DATA_matrix_Prof, DATA_matrix_Act)
    ######################################################
    
    #Escribir los parámetros en un archivo JSON...
    dbr.F_create_param_file(DATA_matrix_Act, DATA_matrix_Prof, DATA_matrix_Cent,
                            DATA_matrix_Weeks, DATA_matrix_Pract, DATA_list_Lin,
                            st.param_path_list)
    ######################################################
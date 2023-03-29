from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random

author = 'Your name here'

doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'real_effort_numbers_t_nt'
    num_rounds = 11
    players_per_group = 2
    minimum_substract_approach = 10 
    num_sub_rounds_stage_1 = 10
    pay_per_correct_answer = 100
    list_attr = [
        "correct_answers_round1",
        "correct_answers_round2",
        "correct_answers_round3",
        "correct_answers_round4",
        "correct_answers_round5",
        "correct_answers_round6",
        "correct_answers_round7",
        "correct_answers_round8",
        "correct_answers_round9",
        "correct_answers_round10"
    ]
    
class Group(BaseGroup):
    pass




class Subsession(BaseSubsession):
    
    
    def creating_session(self):
        team_label = ["AB", "CD"] 
        number_of_groups = self.session.num_participants // Constants.players_per_group #Numero de grupos
        ## STAGE 1
        if self.round_number >= 1 and self.round_number <= Constants.num_sub_rounds_stage_1:
            for i in range(0, number_of_groups):
                for j in range(0, Constants.players_per_group):
                    self.get_group_matrix(objects=True)[i][j].team =  team_label[i]


        ##STAGE 2 y 3
        if self.round_number == Constants.num_rounds:
            self.group_randomly(fixed_id_in_group=True) ## Randomizar grupos manteniento el label del jugador
            for i in range(0, number_of_groups):
                for j in range(0, Constants.players_per_group):
                    self.get_group_matrix(objects=True)[i][j].team_stage_2 = team_label[i]



class Player(BasePlayer):
    
    #Variable auxiliar
    team = models.StringField()
    team_stage_2 = models.StringField()
    payment_stage_1 = models.IntegerField(initial=0)
    correct_answers_stage_1 = models.IntegerField(initial=0)

    ##Variables etapa 2
    pay_contract = models.BooleanField(
        label="",
        choices=[
            [True, "Si"],
            [False, "No"]
        ],
        widget = widgets.RadioSelect
    )


    #Variables de restas etapa 1
    #Variables temporales para mostrar en el HTML
    correct_answers_actual_round = models.IntegerField(initial=0) #Valor por defecto en 0 con initial
    total_substract_actual_round = models.IntegerField(initial=0) 
    wrong_substract_actual_round = models.IntegerField(initial=0)
    payment_actual_round = models.IntegerField(initial=0)

    #Variables por cada ronda
    correct_answers_round1 = models.IntegerField(initial=0) 
    correct_answers_round2 = models.IntegerField(initial=0) 
    correct_answers_round3 = models.IntegerField(initial=0) 
    correct_answers_round4 = models.IntegerField(initial=0) 
    correct_answers_round5 = models.IntegerField(initial=0) 
    correct_answers_round6 = models.IntegerField(initial=0) 
    correct_answers_round7 = models.IntegerField(initial=0) 
    correct_answers_round8 = models.IntegerField(initial=0)
    correct_answers_round9 = models.IntegerField(initial=0)
    correct_answers_round10 = models.IntegerField(initial=0) 

    def other_player(self):  #Obtener el otro jugador del grupo
        # get_others_in_group() = [Player2]
        return self.get_others_in_group()[0]   ## Grupos de dos  

    numero_identificacion = models.IntegerField(label="Coloque su numero de identificacion", blank=True)
    aceptar_dato = models.BooleanField(
        label="¿Desea aceptar el tratamiento de datos?", 
        choices=[
            [True, "Verdadero"],
            [False, "Falso"]
        ]
    )

    control_1 = models.IntegerField(
        label="¿Estaré emparejado con la misma persona en toda la Etapa 1?",
        choices=[
            [1, "Si"],
            [2, "No"]
        ],
        widget=widgets.RadioSelect
    )

    control_2 = models.IntegerField(
        label="Si en la ronda 1, mi compañero(a) y yo logramos 20 restas correctas, cada uno ganará:",
        choices=[
            [2000, "2000"],
            [1000, "1000"],
            [3000, "3000"]
        ],
        widget=widgets.RadioSelect
    )

    ## TODO: Mensajes de error pero que deje continuar la interaccion

    ######### Validaciones
    def aceptar_dato_error_message(self, valor):
        if valor == False:
            return "Debe aceptar los terminos y condiciones"
        
    def control_1_error_message(self, valor):
        if valor == 2:
            return "Ponga cuidado"
    
    def control_2_error_message(self, valor):
        if valor != 1000:
            return "Aprenda a multiplicar"






    
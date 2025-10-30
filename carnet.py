from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD

car_model = DiscreteBayesianNetwork(
    [
        ("Battery", "Radio"),
        ("Battery", "Ignition"),
        ("Ignition","Starts"),
        ("Gas","Starts"),
        ("Starts","Moves"),
        ("KeyPresent","Starts"),

])

# Defining the parameters using CPT

cpd_keyPresent =TabularCPD(
    variable = "KeyPresent", variable_card = 2, values=[[0.7],[0.3]],
    state_names = {"KeyPresent": ['yes', "no"]},
)
cpd_battery = TabularCPD(
    variable="Battery", variable_card=2, values=[[0.70], [0.30]],
    state_names={"Battery":['Works',"Doesn't work"]},
)

cpd_gas = TabularCPD(
    variable="Gas", variable_card=2, values=[[0.40], [0.60]],
    state_names={"Gas":['Full',"Empty"]},
)

cpd_radio = TabularCPD(
    variable=  "Radio", variable_card=2,
    values=[[0.75, 0.01],[0.25, 0.99]],
    evidence=["Battery"],
    evidence_card=[2],
    state_names={"Radio": ["turns on", "Doesn't turn on"],
                 "Battery": ['Works',"Doesn't work"]}
)

cpd_ignition = TabularCPD(
    variable=  "Ignition", variable_card=2,
    values=[[0.75, 0.01],[0.25, 0.99]],
    evidence=["Battery"],
    evidence_card=[2],
    state_names={"Ignition": ["Works", "Doesn't work"],
                 "Battery": ['Works',"Doesn't work"]}
)

cpd_starts = TabularCPD(
    variable="Starts",
    variable_card=2,
    values=[[0.99, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99]],
    evidence=["Ignition", "Gas","KeyPresent"],
    evidence_card=[2, 2, 2],
    state_names={"Starts":['yes','no'], "Ignition":["Works", "Doesn't work"], "Gas":['Full',"Empty"], "KeyPresent": ["yes" ,"no"],},
)

cpd_moves = TabularCPD(
    variable="Moves", variable_card=2,
    values=[[0.8, 0.01],[0.2, 0.99]],
    evidence=["Starts"],
    evidence_card=[2],
    state_names={"Moves": ["yes", "no"],
                 "Starts": ['yes', 'no'] }
)


# Associating the parameters with the model structure
car_model.add_cpds( cpd_starts,cpd_keyPresent, cpd_ignition, cpd_gas, cpd_radio, cpd_battery, cpd_moves)

car_infer = VariableElimination(car_model)

print(car_infer.query(variables=["Moves"],evidence={"Radio":"turns on", "Starts":"yes"}))

def main():
    infer = VariableElimination(car_model)

    # Given that the car will not move, probability that the battery is not working
    q1 = infer.query(variables=["Battery"], evidence={"Moves": "no"})
    print("1.P(Battery | Moves=no):")
    print(q1)
    print()

    #Given that the radio is not working, probability that the car will not start
    q2 = infer.query(variables=["Starts"], evidence={"Radio": "Doesn't turn on"})
    print("2.P(Starts | Radio=Doesn't turn on):")
    print(q2)
    print()

    #Given that the battery is working, does the probability of radio working change if gas is present?
    q3a = infer.query(variables=["Radio"], evidence={"Battery" : "Works"})
    print("3a.P(Radio | Battery=Works):")
    print(q3a)
    print()
    q3b = infer.query(variables=["Radio"], evidence={"Battery" : "Works", "Gas": "Full"})
    print("3b.P(Radio | Battery=Works, Gas=Full):")
    print(q3b)
    print()

    #Given that the car doesn't move, how does the probability of ignition failing change if the car has no gas?
    q4a = infer.query(variables=["Ignition"], evidence={"Moves" : "no"})
    print("4a.P(Ignition | Moves=no):")
    print(q4a)
    print()
    q4b = infer.query(variables=["Ignition"], evidence={"Moves" : "no", "Gas" : "Empty"})
    print("4b.P(Ignition | Moves=no, Gas=Empty):")
    print(q4b)
    print()

    #Probability that the car starts if the radio works and it has gas
    q5 = infer.query(variables=["Starts"], evidence={"Radio": "turns on", "Gas": "Full"})
    print("5.P(Starts | Radio=turns on, Gas=Full):")
    print(q5)
    print()

    q6 = infer.query(variables = ["KeyPresent"],evidence={"Moves" : "no"})
    print("6. P(KeyPresent = no | Moves = no:")
    print(q6)
    print()

if __name__ == "__main__":
    main()    
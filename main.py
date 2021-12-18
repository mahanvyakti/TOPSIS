import math
matrix, weights, beneficial  = [], [], []

def create_matrix():
    """
    Accepts alternatives and criteria from the user
        and creates the corresponding matrix.
        
        Parameters:
        ------- 
            none

        Returns:
        -------
        `alternatives`: list of names of alternatives
        `criteria`: list of names of criteria
    """
    alternatives = input("Enter alternatives separated by space:\t").split(" ")
    criteria = input("Enter criteria separated by space:\t").split(" ")
    
    for alt in alternatives:
        criteria_of_alt = []
        print("\nEnter criteria values for alternative " + alt)    
        for crit in criteria:
            value = float(input("Enter value of " + crit + "\t"))
            criteria_of_alt.append(value)
        matrix.append(criteria_of_alt)
    
    return alternatives, criteria

def get_weigths(criteria):
    """Accepts weights for all the criterion from the user.
        
        Parameters:
        ------- 
            `criteria`: list of names of criteria

        Returns:
        -------
            none
    """
    print("\nEnter weights:")
    for criterion in criteria:
        weight = float(input("Enter weight for " + criterion + "\t"))
        weights.append(weight)

def get_b_or_nb(criteria):
    """Accepts whether each criteria is beneficial or non-beneficial
      from the user.
        
        Parameters:
        ------- 
            `criteria`: list of names of criteria

        Returns:
        -------
            none
    """
    print("\n\nEnter if a criterion is beneficial or non-benficial")
    print("Enter y if benficial, n if not.")
    for criterion in criteria:
        while True:
            is_beneficial = input("\nIs " + criterion + " beneficial? (y/n)\t").upper()
            if is_beneficial == "Y":
                beneficial.append(True)
                break
            elif is_beneficial == "N":
                beneficial.append(False)
                break
            else:
                print("Please enter y or n!!")

def get_inputs():
    """
        Combines all the input functons in one.
        
        Parameters:
        ------- 
            none

        Returns:
        -------
        `alternatives`: list of names of alternatives
        `criteria`: list of names of criteria
    """
    alternatives, criteria = create_matrix()
    get_weigths(criteria)
    get_b_or_nb(criteria)

    return alternatives, criteria

def normalize_matrix(alternatives, criteria):
    """
        Performs Column-wise normalization of the input
        matrix created.
        Normalized Value= Original Value/root square sum of all column values
       
        Parameters:
        ------- 
        `alternatives`: list of names of alternatives
        `criteria`: list of names of criteria

        Returns:
        -------
        'normalized_matrix': Matrix containing all the normalized values
    """
    root_squared_sums = [] 

    for crit_index in range(len(criteria)):
        squared_sum = 0
        for alt_index in range(len(alternatives)):
            squared_sum += math.pow(matrix[alt_index][crit_index], 2)
        
        root_squared_sums.append(math.sqrt(squared_sum))

    normalized_matrix = []
    for i in range(len(alternatives)):
        normalized_values = []
        for j in range(len(criteria)):
            normalized_values.append(matrix[i][j] / root_squared_sums[j])
        normalized_matrix.append(normalized_values)

    return normalized_matrix

def weighted_normalization(normalized_matrix):
    """
        Performs Multiplication of each normalized value 
        with its corresponding criteria weight.
        
        Parameters:
        ------- 
        `alternatives`: list of names of alternatives
        `criteria`: list of names of criteria

        Returns:
        -------
        'weight_normalized_matrix': Matrix formed after multiplication 
                                    of values and weight
    """
    weight_normalized_matrix = []
    
    for row in normalized_matrix:
        wt_norm_values = []
        for (index, norm_val) in enumerate(row):
            weighted_value = norm_val * weights[index]
            wt_norm_values.append(weighted_value)
        
        weight_normalized_matrix.append(wt_norm_values)

    return weight_normalized_matrix

def get_best_and_worst_alteratives(wt_norm_matrix):
    """
      Selects j_plus and j_minus values  for each criteria depending 
      on whether it is beneficial or non-beneficial.
      For Beneficial: j_plus= max value; j_minus= min value
      For Non-Beneficial: j_plus= min value; j_minus= max value
       
        Parameters:
        ------- 
        'weight_normalized_matrix': Matrix formed after multiplication 
                                    of values and weight

        Returns:
        -------
        'j_plus': list of all j_plus of each criteria depending on beneficial or non-beneficial
        'j_minus': list of all j_minus of each criteria depending on beneficial or non-beneficial
    """
    new_matrix = list(zip(*wt_norm_matrix)) # Take transpose
    j_plus, j_minus = [], []

    for (crit_index, criterion_values) in enumerate(new_matrix[:]):
        max_val = max(criterion_values)
        min_val = min(criterion_values)

        j_plus.append(max_val if beneficial[crit_index] else min_val)
        j_minus.append(min_val if beneficial[crit_index] else max_val)
    
    return j_plus, j_minus

def get_l2_distances(wt_norm_matrix, j_plus, j_minus):

    """
      Calculates distance from best solution and distance from worst solution
      for each alternative.
       
        Parameters:
        ------- 
        'weight_normalized_matrix': Matrix formed after multiplication 
                                    of values and weight
        'j_plus': list of all j_plus of each criteria depending on beneficial or non-beneficial
        'j_minus': list of all j_minus of each criteria depending on beneficial or non-beneficial

        Returns:
        -------
        'dib': distance from best value for each alternative
        'diw': distance from worst value for each alternative
    """
    diw, dib = [], []   
    for row in wt_norm_matrix:
        best_diff_sum, worst_diff_sum = 0, 0
        for (crit_index, value) in enumerate(row):
            best_diff_sum += math.pow(value - j_plus[crit_index] , 2)
            worst_diff_sum += math.pow(value - j_minus[crit_index] , 2)
        
        dib.append(math.sqrt(best_diff_sum))
        diw.append(math.sqrt(worst_diff_sum))
 
    return dib ,diw

def calculate_similarity(dib, diw):
    """
      Calculates similarity with best value for each alternative.
       
        Parameters:
        ------- 
        'dib': distance from best value for each alternative
        'diw': distance from worst value for each alternative

        Returns:
        -------
        'siw': similarity values for each alternative
    """
    return [(diw[i]/(dib[i]+diw[i])) for i in range(len(dib))]

def sortResults(alternatives, siw):
    """
      Sorts the Alternatives with respect to corresponding siw values in reverse order.
       
        Parameters:
        ------- 
        `alternatives`: list of names of alternatives
        'siw': similarity values for each alternative

        Returns:
        -------
       'sortedRes': Sorted List of Alternatives and siw values
    """
    sortedRes = []
    for i in range(len(alternatives)):
        sortedRes.append([alternatives[i], siw[i]])
    
    sortedRes=sorted(sortedRes, reverse=True,  key=lambda x:x[1])

    return sortedRes

def printResults(sortedRes):
    """
      Prints the sorted list with corresponding ranking
       
        Parameters:
        ------- 
       'sortedRes': Sorted List of Alternatives and siw values

        Returns:
        -------
        none
    """
    print("\nThe Ranking:")
    print("Sr. No.\t\tAlternative\tsiw")
    for (index, name_siw_pair) in enumerate(sortedRes):
        print(str(index + 1) + ".\t\t" + name_siw_pair[0], "\t\t" + str(name_siw_pair[1]))

if __name__ == "__main__":
    alternatives, criteria = get_inputs()
    normalized_matrix = normalize_matrix(alternatives, criteria)
    weight_normalized_matrix = weighted_normalization(normalized_matrix)
    j_plus, j_minus = get_best_and_worst_alteratives(weight_normalized_matrix)
    dib ,diw = get_l2_distances(weight_normalized_matrix, j_plus, j_minus)
    siw = calculate_similarity(dib, diw)
    sortedRes = sortResults(alternatives, siw)
    printResults(sortedRes)

import json
import pygame

def getCommandes():
    controles = {}
    f = open('asset/donnees.json', 'r')
    data = json.load(f)
    f.close()
    for a in data["controles"]:
        controles[a] = data["controles"][a]
    return controles

def getBestScore():
    f = open('asset/donnees.json', 'r')
    data = json.load(f)
    f.close()
    best_score = data["best_score"]
    return best_score

def getSoundState():
    state = []
    f = open('asset/donnees.json', 'r')
    data = json.load(f)
    f.close()
    for a in data["sond_state"]:
        state.append(data["sond_state"][a])
    return state

def newValue(action, touche):
    f = open('asset/donnees.json', 'r')
    data = json.load(f)
    f.close()
    # vérifie si la touche n'est pas déjà associé à une action
    ok = True
    for a in data["controles"]:
        if data["controles"][a] == pygame.key.key_code(touche):
            ok = False
    # Modifie ou non le fichier json
    if ok :
        f = open('asset/donnees.json', 'w')
        data["controles"][action] = pygame.key.key_code(touche)
        json.dump(data, f)
        f.close()
        return touche
    else :
        return pygame.key.name(data["controles"][action])

def newBestScore(score):
    # récupère les données
    f = open('asset/donnees.json', 'r')
    data = json.load(f)
    f.close()
    # change la valeur du meilleur score
    data["best_score"] = score
    # remplace la valeur
    f = open('asset/donnees.json', 'w')
    json.dump(data, f)
    f.close()

def newSoundState(sound, state):
    # récupère les données
    f = open('asset/donnees.json', 'r')
    data = json.load(f)
    f.close()
    # change la valeur du meilleur score
    data["sond_state"][sound] = state
    # remplace la valeur
    f = open('asset/donnees.json', 'w')
    json.dump(data, f)
    f.close()
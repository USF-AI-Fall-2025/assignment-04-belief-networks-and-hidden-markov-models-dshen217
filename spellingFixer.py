
from collections import defaultdict
import math

def train(filename="aspell.txt"):
    # read the file and count transitions/emissions
    transitions = {}
    emissions = {}
    trans_count = {}
    emit_count = {}
    
    lines = 0
    with open(filename) as f:
        for line in f:
            line = line.strip().replace(":", " ").replace(",", " ")
            parts = line.split()
            if len(parts) < 2:
                continue
                
            correct = parts[0].lower()
            typos = [t.lower() for t in parts[1:]]
            lines += 1
            
            # count letter transitions with start and end markers
            # add special START and END markers
            if "START" not in transitions:
                transitions["START"] = {}
            if correct[0] not in transitions["START"]:
                transitions["START"][correct[0]] = 0
            transitions["START"][correct[0]] += 1
            if "START" not in trans_count:
                trans_count["START"] = 0
            trans_count["START"] += 1
            
            # transitions between letters in the word
            for i in range(len(correct)-1):
                a = correct[i]
                b = correct[i+1]
                if a not in transitions:
                    transitions[a] = {}
                if b not in transitions[a]:
                    transitions[a][b] = 0
                transitions[a][b] += 1
                if a not in trans_count:
                    trans_count[a] = 0
                trans_count[a] += 1
            
            # transition from last letter to END
            last = correct[-1]
            if last not in transitions:
                transitions[last] = {}
            if "END" not in transitions[last]:
                transitions[last]["END"] = 0
            transitions[last]["END"] += 1
            if last not in trans_count:
                trans_count[last] = 0
            trans_count[last] += 1
            
            # count emissions from typos
            for typo in typos:
                length = min(len(correct), len(typo))
                for i in range(length):
                    c = correct[i]
                    t = typo[i]
                    if c not in emissions:
                        emissions[c] = {}
                    if t not in emissions[c]:
                        emissions[c][t] = 0
                    emissions[c][t] += 1
                    if c not in emit_count:
                        emit_count[c] = 0
                    emit_count[c] += 1
            
            # also count correct letters (most letters are typed right)
            for char in correct:
                if char not in emissions:
                    emissions[char] = {}
                if char not in emissions[char]:
                    emissions[char][char] = 0
                emissions[char][char] += 1
                if char not in emit_count:
                    emit_count[char] = 0
                emit_count[char] += 1
    
    print(f"Lines used to train: {lines}")
    
    # convert counts to probabilities
    trans_probs = {}
    for a in transitions:
        trans_probs[a] = {}
        for b in transitions[a]:
            trans_probs[a][b] = transitions[a][b] / trans_count[a]
    
    emit_probs = {}
    for a in emissions:
        emit_probs[a] = {}
        for t in emissions[a]:
            emit_probs[a][t] = emissions[a][t] / emit_count[a]
    
    return trans_probs, emit_probs


def viterbi(word, letters, trans_probs, emit_probs):
    # use viterbi to find most likely correct spelling
    word = word.lower()
    n = len(word)
    
    # had issues with probabilities getting too small, using log helped
    V = [{}]
    paths = {}
    
    # start with first letter
    for letter in letters:
        if '^' in trans_probs and letter in trans_probs['^']:
            t_prob = trans_probs['^'][letter]
        else:
            t_prob = 0.000001
            
        if letter in emit_probs and word[0] in emit_probs[letter]:
            e_prob = emit_probs[letter][word[0]]
        else:
            e_prob = 0.00000001
            
        V[0][letter] = math.log(t_prob) + math.log(e_prob)
        paths[letter] = [letter]
    
    # go through rest of word
    for i in range(1, n):
        V.append({})
        new_paths = {}
        
        for curr in letters:
            if curr in emit_probs and word[i] in emit_probs[curr]:
                e_prob = emit_probs[curr][word[i]]
            else:
                e_prob = 0.00000001
            
            best = float('-inf')
            best_prev = None
            
            for prev in letters:
                if prev in trans_probs and curr in trans_probs[prev]:
                    t_prob = trans_probs[prev][curr]
                else:
                    t_prob = 0.000001
                    
                prob = V[i-1][prev] + math.log(t_prob) + math.log(e_prob)
                if prob > best:
                    best = prob
                    best_prev = prev
            
            V[i][curr] = best
            new_paths[curr] = paths[best_prev] + [curr]
        
        paths = new_paths
    
    # find best last letter
    best = float('-inf')
    best_letter = None
    for letter in letters:
        if letter in trans_probs and '$' in trans_probs[letter]:
            t_prob = trans_probs[letter]['$']
        else:
            t_prob = 0.000001
            
        prob = V[-1][letter] + math.log(t_prob)
        if prob > best:
            best = prob
            best_letter = letter
    
    return ''.join(paths[best_letter])


def main():
    trans_probs, emit_probs = train("aspell.txt")
    letters = list("abcdefghijklmnopqrstuvwxyz")
    
    print("Spelling corrector ready")
    print("Type 'quit' to exit\n")
    
    while True:
        text = input("Enter text: ").strip()
        if text.lower() == "quit":
            break
        
        words = text.split()
        fixed = []
        
        for word in words:
            clean = ''.join(c for c in word if c.isalpha())
            if clean:
                corrected = viterbi(clean, letters, trans_probs, emit_probs)
                fixed.append(corrected)
            else:
                fixed.append(word)
        
        print(f"Original:  {text}")
        print(f"Corrected: {' '.join(fixed)}\n")


if __name__ == "__main__":
    main()
import mido
import random
import sys
from os.path import exists



class MidiRandomizer:
    parameters=[]
    deltaVariation=0
    programMode=""
    stringInput=""
    stringOutput=""

    nInstruments=0
    instruments={
            "piano":{0:"Acoustic Grand Piano",1:"Bright Acoustic Piano",2:"Electric Grand Piano",3:"Honky-tonk Piano",
            4:"Electric Piano 1",5:"Electric Piano 2",6:"Harpsichord",7:"Clavinet"},
            
            "Chromatic Percussion":{8:"Celesta",9:"Glockenspiel",10:"Music Box",11:"Vibraphone",12:"Marimba",13:"Xylophone",
            14:"Tubular Bells",15:"Dulcimer"},

            "Organ":{16:"Drawbar Organ",17:"Percussive Organ",18:"Rock Organ",19:"Church Organ",20:"Reed Organ",21:"Accordion",
            22:"Harmonica",23:"Tango Accordion"},

            "Guitar":{24:"Acoustic Guitar (nylon)",25:"Acoustic Guitar (steel)",26:"Electric Guitar (jazz)",
            27:"Electric Guitar (clean)",28:"Electric Guitar (muted)",29:"Electric Guitar (overdriven)",
            30:"Electric Guitar (distortion)",31:"Electric Guitar (harmonics)"},

            "Bass":{32:"Acoustic Bass",33:"Electric Bass (finger)",34:"Electric Bass (picked)",35:"Fretless Bass",36:"Slap Bass 1",
            37:"Slap Bass 2",38:"Synth Bass 1",39:"Synth Bass 2"},

            "Strings":{40:"Violin",41:"Viola",42:"Cello",43:"Contrabass",44:"Tremolo Strings",45:"Pizzicato Strings",
            46:"Orchestral Harp",47:"Timpani"},

            "Ensemble":{48:"String Ensemble 1",49:"String Ensemble 2",50:"Synth Strings 1",51:"Synth Strings 2",52:"Choir Aahs",
            53:"Voice Oohs (or Doos)",54:"Synth Voice or Solo Vox",55:"Orchestra Hit"},

            "Brass":{56:"Trumpet",57:"Trombone",58:"Tuba",59:"Muted Trumpet",60:"French Horn",61:"Brass Section",
            62:"Synth Brass 1",63:"Synth Brass 2"},

            "Reed":{64:"Soprano Sax",65:"Alto Sax",66:"Tenor Sax",67:"Baritone Sax",68:"Oboe",69:"English Horn",
            70:"Bassoon",71:"Clarinet"},

            "Pipe":{72:"Piccolo",73:"Flute",74:"Recorder",75:"Pan Flute",76:"Blown bottle",77:"Shakuhachi",78:"Whistle",
            79:"Ocarina"},

            "Synth Lead":{80:"Lead 1 (square)",81:"Lead 2 (sawtooth)",82:"Lead 3 (calliope)",83:"Lead 4 (chiff)",
            84:"Lead 5 (charang, a guitar-like lead)",85:"Lead 6 (space voice)",86:"Lead 7 (fifths)",87:"Lead 8 (bass and lead)"},

            "Synth Pad":{88:"Pad 1 (new age or fantasia",89:"Pad 2 (warm)",90:"Pad 3 (polysynth or poly)",91:"Pad 4 (choir)",
            92:"Pad 5 (bowed glass or bowed)",93:"Pad 6 (metallic)",94:"Pad 7 (halo)",95:"Pad 8 (sweep)"},

            "Synth Effects":{96:"FX 1 (rain)",97:"FX 2 (soundtrack, a bright perfect fifth pad)",98:"FX 3 (crystal)",
            99:"FX 4 (atmosphere, usually a nylon-like sound)",100:"FX 5 (brightness)",101:"FX 6 (goblins)",
            102:"FX 7 (echoes or echo drops)",103:"FX 8 (sci-fi or star theme)"},

            "Ethnic":{104:"Sitar",105:"Banjo",106:"Shamisen",107:"Koto",108:"Kalimba",109:"Bag pipe",110:"Fiddle",111:"Shanai"},

            "Percussive":{112:"Tinkle Bell",113:"Agogô",114:"Steel Drums",115:"Woodblock",116:"Taiko Drum",
            117:"Melodic Tom or 808 Toms",118:"Synth Drum",119:"Reverse Cymbal"},

            "Sound Effects":{120:"Guitar Fret Noise",121:"Breath Noise",122:"Seashore",123:"Bird Tweet",124:"Telephone Ring",
            125:"Helicopter",126:"Applause",127:"Gunshot"},
            }
    restrictedInstruments=[]

    messages=[]
    def __init__(self,params):
        self.manageParams(params)
    
    def manageParams(self,params):

        for c in range(1,len(params)):
            if params[c] not in self.parameters:
                self.parameters.append(params[c])
            else:
                print("Immissione parametri errata: presenti duplicati")
                self.printManual()
                self.status=1
                return
        if len(self.parameters)==0:
            self.printManual()
            self.status=2
            return
        if "-h" in self.parameters:
            self.printManual()
            self.status=2
            return
        try:
            if len(self.parameters)<4:
                print("Immissione parametri errata: argomenti mancanti")
                self.printManual();
                self.status=1
                return
            if "-t" in self.parameters:
                currentI=self.parameters.index("-t")
                if currentI>len(self.parameters)-3:
                    print("Immissione parametri errata: valore dei ticks non numerico")
                    self.printManual();
                    self.status=1
                    return
                else:
                    if self.parameters[currentI+1].isdigit():
                        self.deltaVariation=int(self.parameters[currentI+1])
                        if (self.deltaVariation!=0):
                            self.messages.append("Variazione ticks : {}".format(self.deltaVariation))
                    else:
                        print("Immissione parametri errata: valore dei ticks non numerico")
                        self.printManual();
                        self.status=1
                        return

            if "-p" in self.parameters:
                currentI=self.parameters.index("-p")
                if currentI>len(self.parameters)-3:
                    print("Immissione parametri errata")
                    self.printManual();
                    self.status=1
                    return
                else:
                    if self.parameters[currentI+1]=="r" or self.parameters[currentI+1]=="t" or self.parameters[currentI+1]=="d":
                        self.programMode=self.parameters[currentI+1]
                        self.messages.append("Strumenti cambiati :");
                        if self.programMode=="d":
                            if exists(self.parameters[currentI+2]):
                                with open(self.parameters[currentI+2],"rt") as f:
                                    restrictedInstruments=eval(f.read())
                                    for k in restrictedInstruments.keys():
                                        for v in restrictedInstruments[k]:
                                            if v not in self.restrictedInstruments:
                                                self.restrictedInstruments.append(v)
                            else:
                                print("Immissione parametri errata: dizionario degli strumenti non trovato")
                                self.printManual()
                                self.status=1
                                return

                    else:
                        print("Immissione parametri errata: valore di sostituzione strumento non riconosciuta")
                        self.printManual();
                        self.status=1
                        return
                    
            if exists(self.parameters[-2]):
                self.stringInput=self.parameters[-2]
            else:
                print("Immissione parametri errata: InputFile non riconosciuto")
                self.printManual();
                self.status=1
                return
            if self.parameters[-1]=="-p" or self.parameters[-1]=="-t": 
                print("Immissione parametri errata")
                self.printManual();
                self.status=1
                return
            else:
                self.stringOutput=self.parameters[-1]
        except:
            print("Immissione parametri errata")
            self.printManual();
            self.status=1
            return
        self.status=0

    def changeProgram(self,oldProgram):
        newProgram=0
        if self.programMode=="r":
            newProgram=random.randint(0,127)
            oldIndex=0
            newIndex=0
            for k in self.instruments.keys():
                if oldProgram in self.instruments[k].keys():
                    oldIndex=k
                if newProgram in self.instruments[k].keys():
                    newIndex=k
            self.messages.append("{}:{} -> {}:{}".format(oldProgram,self.instruments[oldIndex][oldProgram],newProgram,self.instruments[newIndex][newProgram]))
        elif self.programMode=="t":
            for k in self.instruments.keys():
                if oldProgram in self.instruments[k].keys():
                    newProgram=oldProgram
                    while oldProgram==newProgram:
                        newProgram=random.randint(list(self.instruments[k].keys())[0],list(self.instruments[k].keys())[-1])
                    self.messages.append("{}:{} -> {}:{}".format(oldProgram,self.instruments[k][oldProgram],newProgram,self.instruments[k][newProgram]))
        elif self.programMode=="d":
            newProgram=self.restrictedInstruments[random.randint(0,len(self.restrictedInstruments)-1)]

            for k in self.instruments.keys():
                if oldProgram in self.instruments[k].keys():
                    oldIndex=k
                if newProgram in self.instruments[k].keys():
                    newIndex=k
            self.messages.append("{}:{} -> {}:{}".format(oldProgram,self.instruments[oldIndex][oldProgram],newProgram,self.instruments[newIndex][newProgram]))
        return newProgram

    def randomize(self):
        if self.status==1 or self.status==2:
            exit()
        inputMidi=mido.MidiFile(self.stringInput)
        outputMidi=mido.MidiFile()
        currentT=mido.MidiTrack()
        nInstruments=0;
        # programMsg=mido.Message("program_change",program=0,time=0)
        # currentT.append(programMsg)
        # inputMidi.tracks.insert(0,currentT)
        for t in inputMidi.tracks:
            
            if self.programMode!="":
                for msg in t:
                    if msg.type=="program_change":
                        nInstruments+=1
        if nInstruments==0:
            programMsg=mido.Message("program_change",program=0,time=0)
            currentT.append(programMsg)
            inputMidi.tracks.insert(0,currentT)

        for t in inputMidi.tracks:
            currentT=mido.MidiTrack()
            for msg in t:
                if self.deltaVariation!=0:
                    if hasattr(msg,"time"):
                        if msg.time>=self.deltaVariation:
                            msg.time+=random.randint(-self.deltaVariation,self.deltaVariation);
                if self.programMode!="":
                    if msg.type=="program_change":
                        nInstruments+=1
                        oldProgram=msg.program
                        msg.program=self.changeProgram(oldProgram)
                currentT.append(msg)
            outputMidi.tracks.append(currentT)
        outputMidi.ticks_per_beat=inputMidi.ticks_per_beat

        if "-n" not in self.parameters:
            for m in self.messages:
                print(m)
        return outputMidi
    
    def save(self,midiToSave,outputName=""):
        if outputName=="":
            outputName=self.stringOutput
        midiToSave.save(outputName)
    
    def printManual(self):
        print("Midi Randomizer__________by Fraiolefano")
        print("Manuale di utilizzo:")
        print("-t : aggiunge una variazione temporale in ticks")
        print("-p r|t|f : modifica gli strumenti del brano")
        print("   -p r : in modo totalmente R andomico")
        print("   -p t : in modo casuale ma restando nel contesto della T ipologia dello strumento")
        print("   -p d dictFile : in modo casuale utilizzando un D izionario di strumenti salvato in un file")
        print("-n : Non stampare a schermo le modifiche effettuate")
        print("-h : mostra questo manuale")
        print("-"*10)
        
        print("Qualche esempio di utilizzo:");
        print("midiRnd -t 2 inputFile.mid outputFile.mid")
        print("midiRnd -p r inputFile.mid outputFile.mid")
        print("midiRnd -p t inputFile.mid outputFile.mid")
        print("midiRnd -t 10 -p r inputFile.mid outputFile.mid")
        print("midiRnd -t 10 -p t inputFile.mid outputFile.mid")
        print("midiRnd -t 25 -p d dictFile.txt inputFile.mid outputFile.mid")
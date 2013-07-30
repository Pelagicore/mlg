from random import randint

DETERMINERS = ["a few", "a little", "a number of", "a whole 'nother", 
"a whole nother", "all", "almost all", "anny", "anoda", "another", "any", "any and all",
"any ol'", "any old", "any ole", "any-and-all", "atta", "beaucoup", "both",
"bothe", "certain", "couple", "dat", "dem", "dis", "each", "each and every",
"either", "enough", "enuf", "enuff", "eny", "euerie", "everie", "every", "few",
"fewer", "fewest", "fewscore", "fuck all", "hevery", "last", "least", "little",
"many", "many a", "many another", "more", "more and more", "mos'", "most",
"much", "muchee", "nary a", "neither", "next", "nil", "no", "none", "not a little", 
"not even one", "other", "overmuch", "own", "quite a few", "quodque", "said",
"several", "severall", "some", "some ol'", "some old", "some ole", "such",
"sufficient", "that", "them", "these", "they", "thilk", "thine", "this", 
"this, that, and the other", "this, that, or the other", "those", "umpteen",
"us", "various", "wat", "we", "what", "whate'er", "whatever", "which",
"whichever", "yonder", "you"] 

ADJECTIVES = ["able" , "acid" , "angry" , "automatic" , "beautiful" , "black" ,
"boiling" , "bright" , "broken" , "brown" , "cheap" , "chemical" , "chief" ,
"clean" , "clear" , "common" , "complex" , "conscious" , "cut" , "deep" ,
"dependent" , "early" , "elastic" , "electric" , "equal" , "fat" , "fertile" ,
"first" , "fixed" , "flat" , "free" , "frequent" , "full" , "general" , "good"
, "great" , "gray" , "hanging" , "happy" , "hard" , "healthy" , "high" ,
"hollow" , "important" , "kind" , "like" , "living" , "long" , "male" ,
"married" , "material" , "medical" , "military" , "natural" , "necessary" ,
"new" , "normal" , "open" , "parallel" , "past" , "physical" , "political" ,
"poor" , "possible" , "present" , "private" , "probable" , "quick" , "quiet" ,
"ready" , "red" , "regular" , "responsible" , "right" , "round" , "same" ,
"second" , "separate" , "serious" , "sharp" , "smooth" , "sticky" , "stiff" ,
"straight" , "strong" , "sudden" , "sweet" , "tall" , "thick" , "tight" ,
"tired" , "true" , "violent" , "waiting" , "warm" , "wet" , "wide" , "wise" ,
"yellow" , "young" ,"several" , "glorious" , "heavy"]

NOUNS = [ "time" ,"year" ,"people" ,"way" ,"day" ,"man" ,"thing" ,"woman"
,"life" ,"child" ,"world" ,"school" ,"state" ,"family" ,"student" ,"group"
,"country" ,"problem" ,"hand" ,"part" ,"place" ,"case" ,"week" ,"company"
,"system" ,"program" ,"question" ,"work" ,"government" ,"number" ,"night"
,"point" ,"home" ,"water","room ","mother ","area ","money ","story ","fact"
,"month ","lot ","right ","study ","book ","eye ","job ","word ","business" 
,"issue ","side ","kind ","head ","house ","service ","friend ","father" 
,"power ","hour ","game ","line ","end ","member ","law ","car ","city"
,"community","name" ,"president" ,"team" ,"minute" ,"idea" ,"kid" ,"body"
,"information" ,"back" ,"parent" ,"face" ,"others" ,"level" ,"office" ,"door"
,"health" ,"person" ,"art" ,"war" ,"history" ,"party" ,"result" ,"change"
,"morning" ,"reason" ,"research" ,"girl" ,"guy" ,"moment" ,"air" ,"teacher"
,"force" ,"education" ]

ADVERBS = ["up" ,"so" ,"out" ,"just" ,"now" ,"how" ,"then" ,"more" ,"also"
,"here" ,"well" ,"only" ,"very" ,"even" ,"back" ,"there" ,"down" ,"still" ,"in"
,"as" ,"to" ,"when" ,"never" ,"really" ,"most" ,"on" ,"why" ,"about" ,"over"
,"again" ,"where" ,"right" ,"off" ,"always" ,"today" ,"all" ,"far" ,"long"
,"away" ,"yet" ,"often" ,"ever" ,"however" ,"almost" ,"later" ,"much" ,"once"
,"least" ,"ago" ,"together" ,"around" ,"already" ,"enough" ,"both" ,"maybe"
,"actually" ,"probably" ,"home" ,"of course" ,"perhaps" ,"little" ,"else"
,"sometimes" ,"finally" ,"less" ,"better" ,"early" ,"especially" ,"either"
,"quite" ,"simply" ,"nearly" ,"soon" ,"certainly" ,"quickly" ,"no" ,"recently"
,"before" ,"usually" ,"thus" ,"exactly" ,"hard" ,"particularly" ,"pretty"
,"forward" ,"ok" ,"clearly" ,"indeed" ,"rather" ,"that" ,"tonight" ,"close"
,"suddenly" ,"best" ,"instead" ,"ahead" ,"fast" ,"alone" ,"eventually"
,"directly"]

FIRSTNAME = ["William", "Oscar", "Lucas", "Hugo", "Elias", "Alexander", "Liam",
"Charlie", "Oliver", "Filip", "Leo", "Viktor", "Vincent", "Emil", "Axel",
"Anton", "Erik", "Olle", "Theo", "Ludvig", "Isak", "Arvid", "Gustav", "Noah",
"Edvin", "Melvin", "Alfred", "Max", "Albin", "Elliot", "Nils", "Adam",
"Sixten", "Leon", "Wilmer", "Benjamin", "Viggo", "Alvin", "Theodor", "Jacob",
"Valter", "Kevin", "Melker", "Felix", "Simon", "Adrian", "Casper", "Noel",
"Jonathan", "Gabriel", "Alice", "Elsa", "Julia", "Ella", "Maja", "Ebba",
"Emma", "Linnea", "Molly", "Alva", "Wilma", "Agnes", "Klara", "Nellie",
"Isabelle", "Olivia", "Alicia", "Ellen", "Lilly", "Stella", "Freja", "Saga",
"Emilia", "Astrid", "Ida", "Nova", "Moa", "Isabella", "Alma", "Vera", "Signe",
"Elin", "Ester", "Selma", "Ellie", "Amanda", "Sara", "Tyra", "Tuva", "Felicia",
"Matilda", "Elvira", "Leah", "Sofia", "Siri", "Hanna", "Lovisa", "Lova",
"Nora", "Edith"]

SURNAME = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller",
"Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White",
"Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark",
"Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez",
"King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker",
"Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner",
"Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart",
"Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy",
"Bailey", "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres",
"Peterson", "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders",
"Price", "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman",
"Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores",
"Washington", "Butler", "Simmons", "Foster", "Gonzales", "Bryant", "Alexander",
"Russell", "Griffin", "Diaz", "Hayes"] 

def getSentence(length=1):
	""" Generate length number of sentences consisting of 3-4 words """
	s = ""
	for x in range(0,length):
		s = s + DETERMINERS[randint(0, len(DETERMINERS)-1)] + " "
		if randint(1,5) == 1:
			s = s + ADVERBS[randint(0,len(ADVERBS))-1] + " "
		s = s + ADJECTIVES[randint(0,len(ADJECTIVES)-1)] + " "
		s = s + NOUNS[randint(0,len(NOUNS)-1)] + " "
		if length > 1:
			s = s + "."
	return s.title().strip()

def getFirstName():
	""" Get a random first name """
	return FIRSTNAME[randint(0, len(FIRSTNAME)-1)]

def getSurname():
	""" Get a random surname """
	return SURNAME[randint(0, len(SURNAME)-1)]

def getFullName():
	""" Get a random first and surname """
	return "%s %s" % (getFirstName(), getSurname())

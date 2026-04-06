# ---------------------------
# 1. Base Question Pools
# ---------------------------

math_pool = [
    ("What is 1 + 1?", "2"),
    ("What is 5 + 5?", "10"),
    ("What is 10 - 3?", "7"),
    ("What is 2 * 3?", "6"),
    ("What is 20 / 4?", "5"),
    ("What is 15 + 7?", "22"),
    ("What is 9 - 4?", "5"),
    ("What is 3 * 4?", "12"),
    ("What is 18 / 2?", "9"),
    ("What is 6 + 8?", "14"),
]

factual_pool = [
    ("What is the capital of China?", "beijing"),
    ("Who was the first US president?", "george washington"),
    ("What is the largest planet?", "jupiter"),
    ("What is the chemical symbol for water?", "h2o"),
    ("Who wrote Romeo and Juliet?", "william shakespeare"),
    ("What is the square root of 16?", "4"),
    ("What is the currency of Japan?", "yen"),
    ("Who discovered penicillin?", "alexander fleming"),
    ("What is the longest river in the world?", "nile"),
    ("What is the atomic number of carbon?", "6"),
]

linking_pool = [
    {
        "contexts": ["John is near the Statue of Peace.", "The Statue of Peace is in the Northern Park."],
        "question": "Who is at the Northern Park?",
        "answer": "john"
    },
    {
        "contexts": ["The Golden Key is inside the Oak Chest.", "The Oak Chest is in the Attic."],
        "question": "Which room contains the Golden Key?",
        "answer": "attic"
    },
    {
        "contexts": ["Alice lives in the Blue House.", "The Blue House is on Elm Street."],
        "question": "What street does Alice live on?",
        "answer": "elm street"
    },
    {
        "contexts": ["The book is on the shelf.", "The shelf is in the library."],
        "question": "What building is the book in?",
        "answer": "library"
    },
    {
        "contexts": ["Tom has the red ball.", "The red ball is under the table."],
        "question": "Where is Tom's ball?",
        "answer": "under the table"
    },
    {
        "contexts": ["The cat is in the garden.", "The garden is behind the house.", "The house is on Pine Street."],
        "question": "What street is the cat on?",
        "answer": "pine street"
    },
    {
        "contexts": ["Sarah works at the bank.", "The bank is downtown."],
        "question": "What area is Sarah's workplace in?",
        "answer": "downtown"
    },
    {
        "contexts": ["The car is parked in the garage.", "The garage is next to the house.", "The house is on Maple Avenue."],
        "question": "On what avenue is the car parked?",
        "answer": "maple avenue"
    },
    {
        "contexts": ["The treasure is in the chest.", "The chest is in the cave.", "The cave is in the mountain."],
        "question": "Which mountain contains the treasure?",
        "answer": "mountain"
    },
    {
        "contexts": ["The phone is on the desk.", "The desk is in the office.", "The office is in the building."],
        "question": "Which building contains the phone?",
        "answer": "building"
    },
]

# ---------------------------
# 2. Noise & Context Pools
# ---------------------------

fantasy_noise = [
    "The dragon slept atop the silver mountains for a thousand years.",
    "Elara found the glowing herb beneath the roots of the ancient World Tree.",
    "The stars whispered secrets to the sailors of the Midnight Sea.",
    "A wizard cast a spell that turned the river into gold.",
    "The unicorn galloped through the enchanted forest at dawn.",
    "Pirates discovered a hidden island with talking animals.",
    "A fairy granted three wishes to the brave knight.",
    "The phoenix rose from ashes in the volcanic crater.",
    "Mermaids sang melodies that calmed the stormy seas.",
    "Elves crafted magical rings in their underground kingdom.",
    "A giant guarded the bridge to the forbidden castle.",
    "The sorceress brewed potions under the full moon.",
    "Dragons hoarded treasures in cavernous lairs.",
    "Fairies danced in circles around ancient stone circles.",
    "The griffin soared above the misty peaks.",
    "A troll lived under the old stone bridge.",
    "The centaur raced across the open plains.",
    "Witches flew on broomsticks through the night sky.",
    "The goblin king ruled over a subterranean realm.",
    "A phoenix's rebirth cycle lasts five hundred years.",
]

numeric_noise = [
    "1+1=2",
    "5+5=10",
    "10+10=20",
    "Calculated values: X=5",
    "Y=10",
    "Z=15",
    "Prime sequence: 2",
    "3",
    "5",
    "7",
    "11",
    "13",
    "Fibonacci numbers: 1, 1, 2, 3, 5, 8",
    "Pi is approximately 3.14159",
    "The speed of light is 299792458 meters per second",
    "Avogadro's number is 6.02214076e23",
    "Euler's number e is 2.71828",
    "Square of 2 is 4",
    "Cube of 3 is 27",
    "Factorial of 5 is 120",
    "The sum of angles in a triangle is 180 degrees",
    "There are 365 days in a year",
    "A circle has 360 degrees",
    "The boiling point of water is 100 degrees Celsius",
    "The freezing point of water is 0 degrees Celsius",
]

geography_noise = [
    "The capital of France is Paris",
    "Egypt's capital is Cairo",
    "Brazil is the largest country in South America",
    "The Nile is the longest river in the world",
    "The Amazon is the second longest river",
    "Australia is both a country and a continent",
    "The Sahara is the largest desert",
    "Mount Everest is the highest mountain",
    "The Pacific Ocean is the largest ocean",
    "Antarctica is the coldest continent",
    "The equator divides the Earth into Northern and Southern Hemispheres",
    "Greenland is the largest island",
    "Russia spans eleven time zones",
    "The Dead Sea is the lowest point on Earth",
    "Japan consists of over 6,800 islands",
    "The Grand Canyon is in Arizona, USA",
    "The Amazon rainforest produces 20% of the world's oxygen",
    "Iceland is located on the Mid-Atlantic Ridge",
    "The Himalayas contain ten of the world's highest peaks",
    "Lake Baikal is the deepest lake in the world",
    "The Atacama Desert is the driest place on Earth",
    "Venice is built on 118 islands",
    "The Great Wall of China is visible from space",
    "Australia has the most venomous snakes",
    "The Maldives is the lowest country above sea level",
]

# ---------------------------
# 3. Info-Question Pool
# ---------------------------

info_question_pool = [
    {
        "info": "The book on the table has a blue cover.",
        "question": "What is the color of the book on the table?",
        "answer": "blue"
    },
    {
        "info": "John is 25 years old.",
        "question": "How old is John?",
        "answer": "25"
    },
    {
        "info": "The cat is sleeping on the couch.",
        "question": "Where is the cat sleeping?",
        "answer": "on the couch"
    },
    {
        "info": "The meeting starts at 3 PM.",
        "question": "What time does the meeting start?",
        "answer": "3 pm"
    },
    {
        "info": "Sarah lives in a red house.",
        "question": "What color is Sarah's house?",
        "answer": "red"
    },
    {
        "info": "The train arrives at platform 5.",
        "question": "At which platform does the train arrive?",
        "answer": "5"
    },
    {
        "info": "Tom has three apples.",
        "question": "How many apples does Tom have?",
        "answer": "three"
    },
    {
        "info": "The movie lasts for two hours.",
        "question": "How long does the movie last?",
        "answer": "two hours"
    },
    {
        "info": "The dog is named Max.",
        "question": "What is the dog's name?",
        "answer": "max"
    },
    {
        "info": "The restaurant is located on Main Street.",
        "question": "On which street is the restaurant located?",
        "answer": "main street"
    },
    {
        "info": "Lisa wears a green dress.",
        "question": "What color dress does Lisa wear?",
        "answer": "green"
    },
    {
        "info": "The package weighs 5 kilograms.",
        "question": "How much does the package weigh?",
        "answer": "5 kilograms"
    },
    {
        "info": "The room has four windows.",
        "question": "How many windows does the room have?",
        "answer": "four"
    },
    {
        "info": "The car is parked in spot 12.",
        "question": "In which spot is the car parked?",
        "answer": "12"
    },
    {
        "info": "Mike plays the guitar.",
        "question": "What instrument does Mike play?",
        "answer": "guitar"
    },
    {
        "info": "The flight departs at 8 AM.",
        "question": "What time does the flight depart?",
        "answer": "8 am"
    },
    {
        "info": "The cake is chocolate flavored.",
        "question": "What flavor is the cake?",
        "answer": "chocolate"
    },
    {
        "info": "Anna has long hair.",
        "question": "What kind of hair does Anna have?",
        "answer": "long"
    },
    {
        "info": "The store opens at 9 AM.",
        "question": "What time does the store open?",
        "answer": "9 am"
    },
    {
        "info": "The bicycle has two wheels.",
        "question": "How many wheels does the bicycle have?",
        "answer": "two"
    }
]

# ---------------------------
# 4. John Apple List (Context + Change)
# ---------------------------

john_apple_list = [
    {"context": "John receives 2 apples", "change": 2},
    {"context": "John throws away 1 apple", "change": -1},
    {"context": "John buys 5 apples from the store", "change": 5},
    {"context": "John finds 3 apples in the garden", "change": 3},
    {"context": "John eats 2 apples", "change": -2},
    {"context": "John gives away 4 apples", "change": -4},
    {"context": "Tom gives John 6 apples", "change": 6},
    {"context": "John loses 1 apple by accident", "change": -1},
    {"context": "John trades 3 apples with Sarah", "change": -3},
    {"context": "John picks 7 apples from the tree", "change": 7},
    {"context": "John receives 4 apples from his friend", "change": 4},
    {"context": "John stole 5 apples from the store", "change": 5},
    {"context": "Sarah gives John 2 apples", "change": 2},
    {"context": "John uses 3 apples for cooking", "change": -3},
    {"context": "John sells 2 apples at the market", "change": -2},
    {"context": "The store delivers 10 apples to John", "change": 10},
    {"context": "John spoils 1 apple", "change": -1},
    {"context": "John gets 4 more apples as a gift", "change": 4},
    {"context": "John removes 2 bad apples", "change": -2},
    {"context": "John receives 3 fresh apples", "change": 3},
    {"context": "John donates 5 apples to the food bank", "change": -5},
    {"context": "John harvests 6 apples", "change": 6},
    {"context": "John shares 2 apples with his family", "change": -2},
    {"context": "John collects 9 apples", "change": 9},
    {"context": "John discards 3 rotten apples", "change": -3},
    {"context": "John purchases 7 apples", "change": 7},
    {"context": "John loses 2 apples in the bag", "change": -2},
    {"context": "John gets handed 4 apples by his neighbor", "change": 4},
    {"context": "John takes 5 apples from the basket", "change": 5},
    {"context": "John puts back 1 apple", "change": -1},
    {"context": "John receives a batch of 8 apples", "change": 8},
    {"context": "John eats 3 apples for lunch", "change": -3},
    {"context": "John finds 2 more apples", "change": 2},
    {"context": "John gets 6 apples from the farmer", "change": 6},
    {"context": "John throws out 2 apples", "change": -2},
    {"context": "John picks up 4 apples from the ground", "change": 4},
    {"context": "John loses 4 apples during transport", "change": -4},
    {"context": "John consumes 2 apples", "change": -2},
    {"context": "John crushes 3 apples for juice", "change": -3},
    {"context": "John loses 1 apple on the way", "change": -1},
    {"context": "John receives 2 more apples", "change": 2},
    {"context": "John cuts 4 apples for a pie", "change": -4},
    {"context": "John gives back 2 apples", "change": -2},
    {"context": "John collects 6 more apples", "change": 6},
]

# ---------------------------
# 5. Fantasy Question Pool
# ---------------------------

fantasy_question_pool = [
    {
        "info": "The magician has a crystal ball that glows blue.",
        "question": "What color does the magician's crystal ball glow?",
        "answer": "blue"
    },
    {
        "info": "The enchanted sword was forged in the volcanic fires of Mount Inferno.",
        "question": "Where was the enchanted sword forged?",
        "answer": "mount inferno"
    },
    {
        "info": "The witch's potion contains eye of newt, frog tongue, and spider silk.",
        "question": "What are the three ingredients in the witch's potion?",
        "answer": "eye of newt, frog tongue, and spider silk"
    },
    {
        "info": "The dragon's hoard contains 500 gold coins.",
        "question": "How many gold coins are in the dragon's hoard?",
        "answer": "500"
    },
    {
        "info": "The wizard lives in a tower made of silver stones.",
        "question": "What material is the wizard's tower made of?",
        "answer": "silver stones"
    },
    {
        "info": "The fairy queen rules over the Enchanted Forest.",
        "question": "What does the fairy queen rule over?",
        "answer": "the enchanted forest"
    },
    {
        "info": "The knight's armor is painted crimson red.",
        "question": "What color is the knight's armor?",
        "answer": "crimson red"
    },
    {
        "info": "The spell requires reciting 7 magic words.",
        "question": "How many magic words does the spell require?",
        "answer": "7"
    },
    {
        "info": "The phoenix rises from its ashes every 100 years.",
        "question": "How often does the phoenix rise from its ashes?",
        "answer": "every 100 years"
    },
    {
        "info": "The cursed amulet brings 13 years of bad luck.",
        "question": "How many years of bad luck does the cursed amulet bring?",
        "answer": "13"
    },
    {
        "info": "The ancient grimoire is bound in dragon leather.",
        "question": "What is the grimoire bound in?",
        "answer": "dragon leather"
    },
    {
        "info": "The goblin king's crown is studded with 12 emeralds.",
        "question": "How many emeralds are on the goblin king's crown?",
        "answer": "12"
    },
    {
        "info": "The spell book contains 300 different spells.",
        "question": "How many spells are in the spell book?",
        "answer": "300"
    },
    {
        "info": "The magical forest is protected by ancient wards.",
        "question": "What protects the magical forest?",
        "answer": "ancient wards"
    },
    {
        "info": "The unicorn's horn can heal any wound.",
        "question": "What can the unicorn's horn do?",
        "answer": "heal any wound"
    },
    {
        "info": "The mermaids sing songs in the language of the sea.",
        "question": "In what language do the mermaids sing?",
        "answer": "the language of the sea"
    },
    {
        "info": "The enchanted mirror shows your true self.",
        "question": "What does the enchanted mirror show?",
        "answer": "your true self"
    },
    {
        "info": "The potion shop is located in the hidden village.",
        "question": "Where is the potion shop located?",
        "answer": "the hidden village"
    },
    {
        "info": "The cursed castle has 99 locked doors.",
        "question": "How many locked doors does the cursed castle have?",
        "answer": "99"
    },
    {
        "info": "The elven king lives for 500 years.",
        "question": "How long does the elven king live?",
        "answer": "500 years"
    }
]

# ---------------------------
# 6. Geography Question Pool (Fictional)
# ---------------------------

geography_question_pool = [
    {
        "info": "Throxia is the capital of Meridonia.",
        "question": "What is the capital of Meridonia?",
        "answer": "throxia"
    },
    {
        "info": "The Velda Lakes are located in Lattania.",
        "question": "Where are the Velda Lakes located?",
        "answer": "lattania"
    },
    {
        "info": "Mount Valoris is the highest mountain in Carenthia.",
        "question": "What is the highest mountain in Carenthia?",
        "answer": "mount valoris"
    },
    {
        "info": "The country of Midland has 52 states.",
        "question": "How many states does Midland have?",
        "answer": "52"
    },
    {
        "info": "The Sapphire Sea borders 17 nations.",
        "question": "How many nations border the Sapphire Sea?",
        "answer": "17"
    },
    {
        "info": "Scoutport is the capital of Velnoth.",
        "question": "What is the capital of Velnoth?",
        "answer": "scoutport"
    },
    {
        "info": "The Crystalpeak Mountains span across Nordmarch.",
        "question": "Which region do the Crystalpeak Mountains span across?",
        "answer": "nordmarch"
    },
    {
        "info": "Thornwick is located at the eastern edge of Silvere.",
        "question": "Where is Thornwick located?",
        "answer": "at the eastern edge of silvere"
    },
    {
        "info": "The Ash Desert covers parts of Graxland, Ostmere, and Darkholm.",
        "question": "Which countries does the Ash Desert cover?",
        "answer": "graxland, ostmere, and darkholm"
    },
    {
        "info": "The Riverflow River flows through Eldoria, Westmark, and Sunhaven.",
        "question": "Which countries does the Riverflow River flow through?",
        "answer": "eldoria, westmark, and sunhaven"
    },
    {
        "info": "Kaeltos is located in Central Valorian.",
        "question": "In which region is Kaeltos located?",
        "answer": "central valorian"
    },
    {
        "info": "The Starlight Canal connects Northumbra to Southmarch.",
        "question": "What does the Starlight Canal connect?",
        "answer": "northumbra to southmarch"
    },
    {
        "info": "Nordmarch has 34 provinces.",
        "question": "How many provinces does Nordmarch have?",
        "answer": "34"
    },
    {
        "info": "The Twilight Ocean is the largest ocean in the known world.",
        "question": "What is the largest ocean in the known world?",
        "answer": "the twilight ocean"
    },
    {
        "info": "Valorheim is the capital of Valorian.",
        "question": "What is the capital of Valorian?",
        "answer": "valorheim"
    },
    {
        "info": "The Obsidian Sea is bordered by 9 countries.",
        "question": "How many countries border the Obsidian Sea?",
        "answer": "9"
    },
    {
        "info": "Frostholm is the capital of Winterland.",
        "question": "What is the capital of Winterland?",
        "answer": "frostholm"
    },
    {
        "info": "The Crimson Desert is in Western Valorian.",
        "question": "In which region is the Crimson Desert located?",
        "answer": "western valorian"
    },
    {
        "info": "The Silverstone Railway is the longest railway line in Meridonia.",
        "question": "What is the longest railway line in Meridonia?",
        "answer": "the silverstone railway"
    },
    {
        "info": "Archon is an island nation situated off the coast of Carenthia.",
        "question": "What is Archon?",
        "answer": "an island nation situated off the coast of carenthia"
    }
]


instruction_pool = [
    {"instruction": "Answer only in Spanish.", "tag": "spanish"},
    {"instruction": "Always respond with exactly the word 'NO'.", "tag": "always_no"},
    {"instruction": "Answer with exactly one word only.", "tag": "one_word"},
    {"instruction": "Always prefix your answer with 'ANSWER:'.", "tag": "prefix_answer"},
    {"instruction": "Respond only in uppercase letters.", "tag": "uppercase"},
    {"instruction": "Always end your answer with '--- END ---'.", "tag": "end_marker"},
    {"instruction": "Respond as if you are a pirate.", "tag": "pirate"},
    {"instruction": "Always include the word 'correct' somewhere in your answer.", "tag": "include_correct"},
    {"instruction": "Answer with only the requested information. Do not repeat the question or add any explanation.", "tag": "answer_only"},
]

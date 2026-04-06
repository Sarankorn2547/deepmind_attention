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
        "question": "Where is the Golden Key?",
        "answer": "attic"
    },
    {
        "contexts": ["Alice lives in the Blue House.", "The Blue House is on Elm Street."],
        "question": "Where does Alice live?",
        "answer": "elm street"
    },
    {
        "contexts": ["The book is on the shelf.", "The shelf is in the library."],
        "question": "Where is the book?",
        "answer": "library"
    },
    {
        "contexts": ["Tom has the red ball.", "The red ball is under the table."],
        "question": "Where is Tom's ball?",
        "answer": "under the table"
    },
    {
        "contexts": ["The cat is in the garden.", "The garden is behind the house."],
        "question": "Where is the cat?",
        "answer": "behind the house"
    },
    {
        "contexts": ["Sarah works at the bank.", "The bank is downtown."],
        "question": "Where does Sarah work?",
        "answer": "downtown"
    },
    {
        "contexts": ["The car is parked in the garage.", "The garage is next to the house.", "The house is on Maple Avenue."],
        "question": "Where is the car parked?",
        "answer": "maple avenue"
    },
    {
        "contexts": ["The treasure is in the chest.", "The chest is in the cave.", "The cave is in the mountain."],
        "question": "Where is the treasure?",
        "answer": "mountain"
    },
    {
        "contexts": ["The phone is on the desk.", "The desk is in the office.", "The office is in the building."],
        "question": "Where is the phone?",
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
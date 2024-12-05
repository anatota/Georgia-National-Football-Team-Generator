# Georgia National Football Team Generator
#### Video Demo:  [Click here for video](https://youtu.be/qHmavsO9maU)
#### Description:
My project generates a football team. In my case, I am using Georgia national football team in order to represent my country. Despite this, the program is written in a way that any team can be generated if the csv file contains following keys: Player, Position, Age, Skill.

The program only accepts csv files and is designed in a way that it stops the program immediately if any other format is provided. First, I missed this case but then I decided the design would be better if I considered it.

My program reads the file and returns a list of dictionary, containing football players' data. The data contains the name of the player, the position they play in, age and skill. Then it asks for formation, sorting option and if the user decides to sort by age, the program will ask if they want to sort by young or old players. The formation validation uses regular expression to validate the input. The input should be something like X-X-X where X is a number. Also, it makes sure there are at least 3 defenders and the sum of numbers (Xs) equal to 10 (since goalkeepers are not included in official formations). Also, if the row contains 4 or 5 players (e.g. X-X-X-X or X-X-X-X-X), the program will also ask the user if they want attacker (forward) oriented or midfielder oriented style. This is done in a way that the program sums up the last two numbers or the middle two numbers, accordingly.

The design I debated the most was while choosing individual players. First, I called that function 4 times like this:
```python
team.append(*choose_player(reader, 'Goalkeeper', 1, sort_by))
team.extend(choose_player(reader, 'Defender', defenders, sort_by))
team.extend(choose_player(reader, 'Midfielder', sum(midfielders), sort_by))
team.extend(choose_player(reader, 'Forward', forwards, sort_by))
```

But then I learned ```zip()``` and ```list.extend()``` functions in python that were not included in the course. Also, I used the global variable ```POSITIONS```. So I changed the code:

```python
for player_num_in_position, position in zip(parsed_formation, POSITIONS):
    args = sort_option, [player for player in players if player['Position'] == f'{position}'], player_num_in_position

    if age is not None:
        args += (age,)
    team.extend(sorted_players(*args))
```

Also, I added the age as an argument if the user would like to sort by age. Therefore, I had to pass ```*args``` as a parameter, because the exact number of arguments were not known, but it would be either 3 or 4.

There are 3 sorting options:
1. Skill
2. Age
3. Random

They have separate functions that deal with these:
1. The skill sorting function reverses the list since it has to choose the players with the highest skill number.
2. Age sorting function has two separate functions: one for young and the second for older players. Therefore, the first one returns the list in ascending, the second one in descending order.
3. The random function uses sample from random library, since the players should occur only once, because they are unique.

Finally, the program outputs the table of players using ```tabulate``` from pip library. The format has grid output.

The project also includes ```test_project.py``` file that tests 4 functions: ```validate_sort, parse, check_format, valid_sum```.

I also learned ```unittest.mock``` that was also mentioned in the course but was not explicitly described. The main skill I acquired during this course was searching things on my own.

That's it and I am very grateful for this course.

# Checkers Game + Machine learning
Implemented checkers game with optimization algorithm to optimizing the evaluation function.
Great thanks to "[Tech With Tim](https://www.youtube.com/watch?v=vnd3RfeG3NM)" youtube channel for its great tutorial about how to make a checkers game.


### Requirements:
* python 3.7
* pygame
```
pip install pygame
```

### Run The Game
Clone this repo:
```shell script
git clone https://github.com/OmidSa75/Checkers_game_with_ML.git
```

To run the game use the following command:
```shell script
python main.py --game_mode [GAME_MODE] --minimax_depth [DEPTH] --epoch [EPOCH]  --lr [LEARNING RATE]
```
##### Game Modes
    * [person2pseron] : play with another person
    * [person2ai] : play with the ai player
    * [ai2ai] : ai plays with itself.
    * [person2ai_ml]: training the evaluation function with playing with ai player. (Not implemented yet)
    * [ai2ai_ml] : ai plays with itself to train its evaluation function.

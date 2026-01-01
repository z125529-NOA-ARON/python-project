# python-project

### Explication of snake_game.py
Function __init__(username, score_manager)
   Store the player's name
   Store the score manager

   Set the window size
   Set the block size

   Load the background image
   Resize the background image

   Load the apple image
   Resize the apple image

   Reset the game
End function

Reset_game function
    Create the snake with a single position
    Set the initial direction
    Set the score to zero
    Generate a random position for the food
    Indicate that the game is in progress
End function

Spawn_food function
    Generate a random x position aligned with the grid
    Generate a random y position aligned with the grid
    Return the position (x, y)
End function

Function move_snake
    Retrieve the position of the head
    Calculate the new position of the head
    Add the new head to the beginning of the snake

    If the head is on the food
        Increment the score
        Generate new food
    Otherwise
        Remove the last segment of the snake
End function


Function check_collisions
    Retrieve the position of the head

    If the head touches the edge of the window
        Return TRUE

    If the head touches the snake's body
        Return TRUE

    Return FALSE
End function


Function start
    Initialise pygame
    Create the game window
    Create the clock (FPS)
    Load the font

    While the game is active
        Retrieve keyboard and window events

        If the window is closed
            Exit the programme

        If a key is pressed
            Update the snake's direction
            If ESC
                Return to the menu

        Move the snake

        If collision detected
            Save the score
            Retrieve the top 4 scores
            Display the Game Over screen
            Exit the game

        Display the background
        Display the snake
        Display the food
        Display the score

        Update the screen
        Limit the game speed
End function

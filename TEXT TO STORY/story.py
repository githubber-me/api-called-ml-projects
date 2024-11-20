#Run in Colab Environment

from transformers import T5Tokenizer, T5ForConditionalGeneration
from huggingface_hub import login

# Set the Hugging Face token
HFTOKEN = "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"
login(token=HFTOKEN)  # Log in with the Hugging Face token

# Load the T5 tokenizer and model using the authentication token
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large", use_auth_token=HFTOKEN)
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", use_auth_token=HFTOKEN)

# Function to generate a story
def generate_story(prompt, audience, length, genre):
    # Preprocessing prompt based on audience and genre
    genre_prompt = f"{genre} story"
    audience_prompt = f"For {audience}s"
    
    # Combine all parts into a single prompt for the model
    full_prompt = f"{audience_prompt}, {genre_prompt}: {prompt}"

    # Tokenize the input prompt
    input_ids = tokenizer(full_prompt, return_tensors="pt").input_ids

    # Generate the story
    outputs = model.generate(input_ids, max_length=length, num_beams=5, no_repeat_ngram_size=2)

    # Decode and return the generated text
    story = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return story

# Terminal-based Interface
def main():
    print("Story Generator")
    print("Here's to generating stories!")

    # Input fields for the user
    prompt = input("Enter your story prompt (one line or one word): ")
    audience = input("Choose the target audience (Adults, Teenagers, Kids): ")
    while audience not in ["Adults", "Teenagers", "Kids"]:
        print("Invalid choice. Please choose from 'Adults', 'Teenagers', or 'Kids'.")
        audience = input("Choose the target audience (Adults, Teenagers, Kids): ")
    
    length = int(input("Choose the length of the story (words, 1-500): "))
    while length < 1 or length > 500:
        print("Please enter a number between 1 and 500.")
        length = int(input("Choose the length of the story (words, 1-500): "))
    
    genre = input("Choose the genre of the story (Fantasy, Adventure, Mystery, Sci-Fi, Horror, Romance): ")
    while genre not in ["Fantasy", "Adventure", "Mystery", "Sci-Fi", "Horror", "Romance"]:
        print("Invalid genre. Please choose from the listed genres.")
        genre = input("Choose the genre of the story (Fantasy, Adventure, Mystery, Sci-Fi, Horror, Romance): ")

    # Generate the story
    print("\nGenerating your story...")
    story = generate_story(prompt, audience, length, genre)
    
    # Display the generated story
    print("\nGenerated Story:")
    print(story)

# Run the main function
if __name__ == "__main__":
    main()

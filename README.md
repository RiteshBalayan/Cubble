# Cubble - Social Connection Concept

Cubble is an open-source, full-stack application designed to foster genuine, meaningful connections in the digital space. This MVP solves the problem of superficial connections by prioritizing conversation over instant judgments, encouraging users to chat first, then decide on potential friendships.

## Overview

Cubble enables users to connect through temporary "bubbles," focusing on conversation before revealing full profiles. This leads to more authentic interactions, unlike traditional swipe-based platforms.

### Key Features

1. **User Profiles**: Basic profile creation and management functionality.
2. **Bubbles**: Users are placed in temporary bubbles based on a set of questions. Each bubble has a 48-hour lifespan and goes through three stages:
    - **Active**: Users engage in group or direct chat within bubbles using confidential profiles.
    - **Voting**: After 48 hours, users can swipe on profiles they liked during the conversation. Once a swipe is mutual, the full profile is revealed.
    - **Archive**: Conversations can be viewed but no longer interacted with.
3. **Real-time Chat**: Integrated real-time chat for group conversations in bubbles and direct messaging with mutual matches.
4. **Friendships**: Once two users mutually swipe each other during the voting stage, they become friends and can continue chatting outside of bubbles.
5. **Rotating Bubbles**: New bubbles form every 48 hours, allowing users to keep meeting new people regularly.


### How It Works
1. Users answer a set of questions to be grouped into bubbles.
2. In the **Active** phase, users can chat with others in the bubble anonymously.
3. After 48 hours, the bubble moves into the **Voting** phase, where users can swipe through profiles and unlock full user profiles.
4. Once voting is complete, the bubble moves to the **Archive** phase, where users can revisit past conversations.
5. New bubbles are formed every 48 hours, encouraging continuous interaction and fresh connections.


### Potential Uses

While Cubble was initially designed for social networking, its core features can be adapted for a variety of use cases, including:

- **Online Gaming**: Use bubbles to group gamers into temporary teams based on skill levels or game preferences. Real-time chat allows for communication within gaming bubbles, and users can become long-term gaming buddies after mutual votes.
- **Community Management**: Cubble can be adapted to manage groups within online communities. Bubbles can act as discussion groups, team assignments, or event-based groupings, encouraging collaboration and deeper interaction.
- **Networking Events**: Use bubbles for time-limited professional networking, where participants engage in discussions first before viewing profiles and deciding on connections.
- **Dating**: Cubble’s model can also be repurposed for dating apps, prioritizing conversation over appearances.

This is just an MVP, and the concept is open-source, meaning that the backend can be modified to suit various forms of connection-making beyond just social apps.

### Technology Stack

- **Backend**: Django
- **Frontend**: Django Template Languge and jquery (Tailwind CSS for responsive, mobile and desktop-enabled UI)
- **Database**: PostgreSQL
- **Open Source**: This is a community-driven project—contributions and improvements are welcome.

### How to Contribute

Cubble is an open-source project, and we encourage developers, designers, and community managers to contribute. Whether it's improving the code, enhancing the UI, or extending the concept into new areas, you're welcome to take this project forward.

Feel free to modify the backend to suit your needs, such as using the core functionality to manage connections in communities, events, or any other setting you can imagine.


1. **Fork the repository**  
    Head to the repository on GitHub and click the "Fork" button at the top right of the page.

2. **Clone your forked repository**
    ```bash
    git clone https://github.com/RiteshBalayan/cubble.git
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your environment variables** (e.g., database settings)

5. **Run migrations**
    ```bash
    python manage.py migrate
    ```

6. **Start the development server**
    ```bash
    python manage.py runserver
    ```

---

## License

Cubble is open-source and available under the [MIT License](./LICENSE). Feel free to use, modify, and distribute it according to the terms of the license.

**Note**: I, Ritesh Balayan, originally co-founded Cubble to address meaningful connection-making in digital spaces. This open-source codebase predates the formation of Cubble Ltd, the company, and is independent of any legal obligations related to the company. While the concept of "bubbles" is open for anyone to use, please note that the word "Cubble" is a trademark of Cubble Ltd in the UK. Feel free to fork this project, adapt the code, and take the concept further as part of your own vision!


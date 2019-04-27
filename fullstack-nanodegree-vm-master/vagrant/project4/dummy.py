from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Item, User
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

#Category for Fishes
category1 = Category(user_id = 1, name = 'Fish')

session.add(category1)
session.commit()

item1 = Item(user_id = 1, name = 'Bass', description = 'Bass (/bæs/) is a name shared by many species of fish. The term encompasses both freshwater and marine species, all belonging to the large order Perciformes, or perch-like fishes. The word bass comes from Middle English bars, meaning "perch".', category = category1)

session.add(item1)
session.commit()

item2 = Item(user_id = 1, name = 'Catfish', description = 'Catfish (or catfishes; order Siluriformes or Nematognathi) are a diverse group of ray-finned fish. Named for their prominent barbels, which resemble a cat\'s whiskers, catfish range in size and behavior from the three largest species alive, the Mekong giant catfish from Southeast Asia, the wels catfish of Eurasia and the piraíba of South America, to detritivores (species that eat dead material on the bottom), and even to a tiny parasitic species commonly called the candiru, Vandellia cirrhosa. There are armour-plated types and there are also naked types, neither having scales. Despite their name, not all catfish have prominent barbels. Members of the Siluriformes order are defined by features of the skull and swimbladder. Catfish are of considerable commercial importance; many of the larger species are farmed or fished for food. Many of the smaller species, particularly the genus Corydoras, are important in the aquarium hobby. Many catfish are nocturnal, but others (many Auchenipteridae) are crepuscular or diurnal (most Loricariidae or Callichthyidae, for example).', category = category1)

session.add(item2)
session.commit()

item3 = Item(user_id = 1, name = 'Tilapia', description = 'Tilapia (/tɪˈlɑːpiə/ tih-LAH-pee-ə) is the common name for nearly a hundred species of cichlid fish from the tilapiine cichlid tribe. Tilapia are mainly freshwater fish inhabiting shallow streams, ponds, rivers, and lakes, and less commonly found living in brackish water. Historically, they have been of major importance in artisanal fishing in Africa, and they are of increasing importance in aquaculture and aquaponics. Tilapia can become a problematic invasive species in new warm-water habitats such as Australia, whether deliberately or accidentally introduced, but generally not in temperate climates due to their inability to survive in cold water.', category = category1)

session.add(item3)
session.commit()

item4 = Item(user_id = 1, name = 'Salmon', description = 'Salmon /ˈsæmən/ is the common name for several species of ray-finned fish in the family Salmonidae. Other fish in the same family include trout, char, grayling and whitefish. Salmon are native to tributaries of the North Atlantic (genus Salmo) and Pacific Ocean (genus Oncorhynchus). Many species of salmon have been introduced into non-native environments such as the Great Lakes of North America and Patagonia in South America. Salmon are intensively farmed in many parts of the world.', category = category1)

session.add(item4)
session.commit()

item5 = Item(user_id = 1, name = 'Eel', description = 'An eel is any ray-finned fish belonging to the order Anguilliformes (/æŋˌɡwɪlɪˈfɔːrmiːz/), which consists of four suborders, 20 families, 111 genera, and about 800 species. Eels undergo considerable development from the early larval stage to the eventual adult stage, and most are predators. The term “eel” originally referred to the European eel, and the name of the order means “European eel-shaped.”', category = category1)

session.add(item5)
session.commit()

item6 = Item(user_id = 1, name = 'Cod', description = 'Cod is the common name for the demersal fish genus Gadus, belonging to the family Gadidae. Cod is also used as part of the common name for a number of other fish species, and some species suggested to belong to genus Gadus are not called cod (the Alaska pollock).', category = category1)

session.add(item6)
session.commit()

item7 = Item(user_id = 1, name = 'Mackerel', description = 'Mackerel is a common name applied to a number of different species of pelagic fish, mostly from the family Scombridae. They are found in both temperate and tropical seas, mostly living along the coast or offshore in the oceanic environment.', category = category1)

session.add(item7)
session.commit()


#Category for Sports
category2 = Category(user_id = 1, name = 'Sport')

session.add(category2)
session.commit()

item1 = Item(user_id = 1, name = 'Association football', description = 'Association football, more commonly known as football or soccer,[a] is a team sport played with a spherical ball between two teams of eleven players. It is played by 250 million players in over 200 countries and dependencies, making it the world\'s most popular sport.The game is played on a rectangular field called a pitch with a goal at each end. The object of the game is to score by moving the ball beyond the goal line into the opposing goal.\nAssociation football is one of a family of football codes, which emerged from various ball games played worldwide since antiquity. The modern game traces its origins to 1863 when the Laws of the Game were originally codified in England by The Football Association. \nPlayers are not allowed to touch the ball with hands or arms while it is in play, except for the goalkeepers within the penalty area. Other players mainly use their feet to strike or pass the ball, but may also use any other part of their body except the hands and the arms. The team that scores most goals by the end of the match wins. If the score is level at the end of the game, either a draw is declared or the game goes into extra time or a penalty shootout depending on the format of the competition. Association football is governed internationally by the International Federation of Association Football, which organises World Cups for both men and women every four years.', category = category2)

session.add(item1)
session.commit()

item2 = Item(user_id = 1, name = 'Basketball', description = 'Basketball is a team sport in which two teams, most commonly of five players each, opposing one another on a rectangular court, compete with the primary objective of shooting a basketball (approximately 9.4 inches (24 cm) in diameter) through the defender\'s hoop (a basket 18 inches (46 cm) in diameter mounted 10 feet (3.048 m) high to a backboard at each end of the court) while preventing the opposing team from shooting through their own hoop. A field goal is worth two points, unless made from behind the three-point line, when it is worth three. After a foul, timed play stops and the player fouled or designated to shoot a technical foul is given one or more one-point free throws. The team with the most points at the end of the game wins, but if regulation play expires with the score tied, an additional period of play (overtime) is mandated.\nPlayers advance the ball by bouncing it while walking or running (dribbling) or by passing it to a teammate, both of which require considerable skill. On offense, players may use a variety of shots—the lay-up, the jump shot, or a dunk; on defense, they may steal the ball from a dribbler, intercept passes, or block shots; either offense or defense may collect a rebound, that is, a missed shot that bounces from rim or backboard. It is a violation to lift or drag one\'s pivot foot without dribbling the ball, to carry it, or to hold the ball with both hands then resume dribbling.\nThe five players on each side at a time fall into five playing positions: the tallest player is usually the center, the tallest and strongest is the power forward, a slightly shorter but more agile big man is the small forward, and the shortest players or the best ball handlers are the shooting guard and the point guard, who implements the coach\'s game plan by managing the execution of offensive and defensive plays (player positioning). Informally, players may play three-on-three, two-on-two, and one-on-one.', category = category2)

session.add(item2)
session.commit()

item3 = Item(user_id = 1, name = 'Table tennis', description = 'TTable tennis, also known as ping-pong, is a sport in which two or four players hit a lightweight ball back and forth across a table using small rackets. The game takes place on a hard table divided by a net. Except for the initial serve, the rules are generally as follows: players must allow a ball played toward them to bounce one time on their side of the table, and must return it so that it bounces on the opposite side at least once. A point is scored when a player fails to return the ball within the rules. Play is fast and demands quick reactions. Spinning the ball alters its trajectory and limits an opponent\'s options, giving the hitter a great advantage.', category = category2)

session.add(item3)
session.commit()

print("added category items!")

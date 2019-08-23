from wordnet_graphql.wordnet_graphql import schema
import json


def read_synset(name):
    return schema.execute('''
        query _ {
            synset(name: "%s") {
                name
                hypernyms {
                    name
                }
                hyponyms {
                    name
                }
            }
        }
    ''' % name).data['synset']


nodes = set()
connections = []

queue = ['linguistics.n.01']

while len(queue) > 0 and len(nodes) < 100:
    synset = read_synset(queue[0])
    nodes.add(synset['name'])
    for s in synset['hypernyms'] + synset['hyponyms']:
        if s['name'] not in nodes:
            queue.append(s['name'])
        nodes.add(s['name'])
        source_idx = list(nodes).index(synset['name'])
        target_idx = list(nodes).index(s['name'])
        connections.append({
            'source': synset['name'],
            'target': s['name']
        })
        
    queue = queue[1:]

print([{'name': n} for n in list(nodes)])
print(connections)
# print('Data saved to file!')

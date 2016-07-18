// Tree + HashMap = Homogeneous Trie
use std::collections::HashMap;
use std::hash::Hash;

#[derive(Debug)]
pub struct Trie<T: Eq + Hash, S: Clone> {
    node: HashMap<T, Trie<T, S>>,
    // optional value at the tip, which is returned while checking a path
    value: Option<S>,
    // marker to check if the path has already been traversed
    // (useful only if all paths have the same depths)
    is_traced_path: bool,
}

impl<T: Eq + Hash, S: Clone> Trie<T, S> {
    pub fn new() -> Trie<T, S> {
        Trie {
            value: None,
            node: HashMap::with_capacity(5),
            is_traced_path: false,
        }
    }

    /* The following methods are tailored for inserting DNA sequences (especially k-mers) */

    pub fn insert_sequence<I: Iterator<Item = T>>(&mut self, mut iterator: I, value: S) {
        match iterator.next() {
            Some(thing) => {
                let mut entry = (&mut self.node).entry(thing).or_insert(Trie::new());
                entry.insert_sequence(iterator, value);
            },
            None => {   // End of iterator: Mark if this is a tip
                if self.value.is_some() && self.node.is_empty() {
                    self.is_traced_path = true;
                } else {
                    self.value = Some(value);
                }
            },
        }
    }

    pub fn find_sequence<I: Iterator<Item = T>>(&self, iterator: I) -> Option<S> {
        let mut current_node = self;
        for thing in iterator {
            if let Some(map) = current_node.node.get(&thing) {
                current_node = &map;
            } else {
                return None
            }
        }

        match current_node.is_traced_path {
            true => None,
            false => current_node.value.clone(),
        }
    }
}

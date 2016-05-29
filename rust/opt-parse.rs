// A simple argument parser which works for most inputs
// Compile it as `rustc -O opt-parse.rs` and point to the directory containing this 'rlib'
// while compiling your binary, like so - `rustc -O <binary> -L <libopt_parse.rlib directory>`
#![crate_type = "rlib"]
#![allow(dead_code)]
use std::collections::HashMap;
use std::env::Args;
use std::iter::repeat;

// assuming we don't 'usually' pass more than 10 args (keeping it simple)
const PROBABLE_SIZE: usize = 10;

pub fn nspace(n: usize) -> String {
    repeat(' ').take(n).collect()
}

// Various options expected from the parser (need to add more, and probably parse them)
#[derive(Eq, PartialEq)]
pub enum ExpectOpt {
    // Indicates some string without a leading 'hyphen' (filenames, for example)
    // FIXME: StringArg should be collected into a `Vec` and supplied as an iterator
    StringArg,
    // Denotes a bool value (i.e., see whether the option exists and don't care about its value)
    // `-d` or `--debug` (for example)
    BoolVal,
    // Get the value corresponding to an option, `-L 10` or `--lines=10`
    StringVal,
}

pub struct ArgsParser {
    // FIXME: doesn't work very well for duplicated options
    // Construct an actual parser, either mark or remove the args from vector once they're parsed
    pub args: Vec<String>,
    // (argument, value)
    parsed_stuff: HashMap<String, String>,
    // (argument, value, help string) - stored only to print the help message
    expected_stuff: Vec<(String, String, String)>,
    usage: String,
    suffix: String,
}

impl ArgsParser {
    // `args_format` is the format of the args passed to your binary (for e.g., "FILE [OPTIONS]")
    // (which will be prefixed by the binary's name while showing the help message)
    pub fn new(mut args: Args, args_format: &str, suffix: &str) -> ArgsParser {
        let name = args.next().unwrap();
        let args_vec = args.collect();
        ArgsParser {
            args: args_vec,
            parsed_stuff: HashMap::with_capacity(PROBABLE_SIZE),
            expected_stuff: Vec::with_capacity(PROBABLE_SIZE),
            usage: format!("USAGE: {} {}", name, args_format),
            suffix: suffix.to_owned(),
        }
    }

    // FIXME: parse the values and display the error (if any) that has occurred
    // Currently, this doesn't point the invalid argument (which should be handled by your binary)
    // `opt_small` is usually a single char option whose value (if any) is followed by a space
    // `opt_big` is usually a key-value pair separated by '='
    // `accessor` is the unique string to which the arg/value should be binded to
    // (you'll get the value corresponding to an option using the `accessor` once parsing is done)
    pub fn update_args(&mut self, opt_small: &str, opt_big: &str, help_msg: &str,
                       accessor: &str, expected: ExpectOpt) {
        let mut args = self.args.iter();
        let mut val_for_opt = "";
        let mut bool_found = false;
        while let Some(arg) = args.next() {
            if arg.starts_with('-') {
                let arg = arg.trim_left_matches('-');
                if arg == opt_small {
                    bool_found = true;
                    match expected {
                        ExpectOpt::StringVal => {
                            if let Some(val) = args.next() {
                                val_for_opt = val;
                            } break
                        }
                        _ => (),
                    }
                }

                let mut arg = arg.split('=');
                if arg.next().unwrap() == opt_big {     // first value always exists in a split!
                    bool_found = true;
                    match expected {
                        ExpectOpt::StringVal => {
                            if let Some(val) = arg.next() {
                                val_for_opt = val;
                            } break
                        }
                        _ => (),
                    }
                }
            } else if opt_small.is_empty() && opt_big.is_empty() {
                if expected == ExpectOpt::StringArg {
                    val_for_opt = arg;
                    break
                }
            }
        }

        self.expected_stuff.push((opt_small.to_owned(), opt_big.to_owned(), help_msg.to_owned()));
        match expected {
            ExpectOpt::BoolVal if !bool_found => (),
            ExpectOpt::StringVal if !bool_found => (),
            _ => {
                let _ = self.parsed_stuff.insert(accessor.to_owned(), val_for_opt.to_owned());
            },
        }
    }

    // check whether an option exists
    pub fn is_opt_exists(&self, accessor: &str) -> bool {
        self.parsed_stuff.get(accessor).is_some()
    }

    // check whether an option exists and get its value (if any)
    pub fn get_val(&self, accessor: &str, error_msg: &str) -> Option<String> {
        match self.parsed_stuff.get(accessor) {
            Some(val) if !val.is_empty() => Some(val.clone()),
            _ => {
                if !error_msg.is_empty() {
                    println!("{}", error_msg);
                    self.show_help();
                } None
            },
        }
    }

    // show the help string for your binary
    // (which shows the formatted version of the args stored in the struct)
    pub fn show_help(&self) {
        let help = self.expected_stuff.iter()
                                      .filter_map(|&(ref arg_small, ref arg_big, ref msg)| {
                                          if arg_small.is_empty() && arg_big.is_empty() {
                                              None
                                          } else {
                                              Some(format!("    -{}{}--{}{}{}",
                                                           arg_small, nspace(6 - arg_small.len() % 6),
                                                           arg_big, nspace(14 - arg_big.len() % 14), msg))
                                          }
                                      }).collect::<Vec<String>>();
        let options = match help.is_empty() {
            true => format!("\n"),
            false => format!("\n\n  OPTIONS:\n{}\n", help.join("\n")),
        };
        println!("\n  {}{}\n{}\n", self.usage, options, self.suffix);
    }
}

# CPrAA - A Checker for Probabilistic Abstract Argumentation

[![PyPI](https://img.shields.io/pypi/v/cpraa "View CPrAA on PyPI")](https://pypi.org/project/cpraa/)

CPrAA is a Python tool and package for various tasks in probabilistic abstract argumentation:
 * find distributions satisfying numerous probabilistic argumentation semantics
 * check for credulous or skeptical acceptance of arguments
 * maximize or minimize the marginal probability of certain arguments
 * generate labellings according to different labelling schemes


## Installation

CPrAA is available on [PyPI](https://pypi.org/project/cpraa/) and can be installed with `pip`:

    pip install cpraa

Note that Python 3.7 or higher is required.


## Basic usage

For usage as a command-line tool, locate your installation of `cpraa` with `pip show cpraa`:

    $ pip show cpraa
    Name: cpraa
    Version: 0.6.1
    [...]
    Location: /path/to/installation

Change to the directory `/path/to/installation/cpraa` and run `python main.py --help` to display the built-in help message of CPrAA.
For the remainder of this readme we assume a shortcut `cpraa` is created which resolves to `python main.py` in this directory.

Basic usage usually requires at least three flags:
   * `--file` (or `-f`) followed by a `.tgf` file specifying the argumentation framework
   * `--semantics` (or `-s`) followed by the names of one or more semantics
   * the task to perform, e.g. `--one_distribution` to compute one distribution which satisfies the constraints of all specified semantics

**Example:**

    $ cpraa --file AFs/example.tgf --semantics MinCmp --one_distribution
    Computing one distribution satisfying the following semantics: MinCmp
    Support:
    P( A,-B, C) = 1

The result shows a distribution in _support format_, that is, only the assignments with non-zero probabilities are shown.
In this case, `P( A,-B, C) = 1` means that the assignment where `A` and `C` hold while `B` does not hold has a probability of one under this distribution.
To get the full distribution, the flag `--distribution_output_format` (or just `-o` for short) can be used with parameter `F`.
Likewise, the parameter `M` can be passed with the same flag to display the marginal probabilities of all arguments, and it is possible to pass multiple format options at once:

    $ cpraa --file AFs/example.tgf --semantics MinCmp --one_distribution --distribution_output_format FM
    Computing one distribution satisfying the following semantics: MinCmp
    P(-A,-B,-C) = 0
    P(-A,-B, C) = 0
    P(-A, B,-C) = 0
    P(-A, B, C) = 0
    P( A,-B,-C) = 0
    P( A,-B, C) = 1
    P( A, B,-C) = 0
    P( A, B, C) = 0
    P(A) = 1
    P(B) = 0
    P(C) = 1


## Input format

Argumentation frameworks (AFs) are provided in trivial graph format (`.tgf`) with some optional extensions.
A simple AF with three nodes (`A`, `B`, `C`) and three edges (`A -> B`, `B -> A`, `B -> C`) is specified as follows:

    A
    B
    C
    #
    A B
    B A
    B C

That is, we first have a declaration of nodes with one node ID per line, then a separator `#`, and finally the declaration of attacks, again with one attack per line.
Empty lines are ignored, and `;` introduces a line comment.

Nodes can optionally be annotated with a name. This can be handy to keep IDs short even if the name is long. 
Further, nodes can be annotated with a numeric value (e.g. `0.75` or `1`) or a value interval (e.g. `0.1:0.3`).
These values or intervals can be used by semantics to impose further constraints. 
Most prominently, the `AF` semantics enforces a node's marginal probability to equal the given value or fall within the specified interval if either is given.

The general format for a node declaration is

> `<node_id>` [ `<node_name>` ] [ `<node_value>` | `<node_value_min>` `:` `<node_value_max>` ] [ `;` `<comment>`]

where `<node_id>` is an alphanumeric string, `<node_name>` is alphanumeric but does not start with a digit, and `<node_value>`, `<node_value_min>`, and `<node_value_max>` are either integers or floats.

Edge declarations consist of two node IDs and can likewise be annotated with a name and a value or an interval:

> `<from_node_id>` `<to_node_id>` [ `<edge_name>` ] [ `<edge_value>` | `<edge_value_min>` `:` `<edge_value_max>` ] [ `;` `<comment>`]

The folder `AFs` contains a number of example argumentation frameworks in `.tgf` format.


## Semantics

The semantics that should be enforced for a task are specified with the `--semantics` or `-s` flag.
There is also the option to specify that certain semantics should _not_ hold with `--complement_semantics` or `-cs`.

A list of all available semantics can be viewed with `--list_semantics` or `-ls`:

    $ cpraa --list_semantics
    Available semantics: Min, Neu, Max, Dirac, Ter, Fou, SFou, Inv, Rat, Coh, Opt, SOpt, Jus, CF, WAdm, PrAdm, MinAdm, JntAdm, WCmp, PrCmp, MinCmp, JntCmp, ElmCF, ElmAdm, ElmCmp, ElmGrn, ElmPrf, ElmSStl, ElmStl, WNorS, NorS, SNorS, WNor, Nor, SNor, AF, NNorAF, NNor, CFs, StrengthCF, StrengthSupportCF, DiracCF, DiracAdm, DiracCmp, DiracGrn, DiracPrf, DiracSStl, DiracStl

Tip: With `--documentation` or `-d` followed by the names of one or more semantics a short description of most semantics is available:

    $ cpraa --documentation Fou MinAdm
    Semantics 'Fou':
        Foundedness semantics: Initial nodes must hold with probability 1.
    
    Semantics 'MinAdm':
        Min-admissibility semantics: CF and for every argument C, P(C) <= min_{B in Pre(C)} P(OR Pre(B)) holds.
        Equivalently, for all B in Pre(C) with Pre(B) = {A1, ..., An}, it holds P(C) <= 1 - P(nA1, ..., nAn).


## Tasks

Before taking a closer look at the tasks offered by CPrAA, it is worth noting that not all tasks are available for all semantics.
This is because, e.g., the optimization tasks are only feasible when facing _linear_ constraints.
However, for some semantics the imposed constraints are polynomial (rendering a formulation in terms of linear constraints impossible), or linear constraints are not yet implemented.
Notably, and perhaps most inconveniently, complement semantics are not available for tasks requiring linear constraints. 


### Check satisfiability 
`-OD`, `--one_distribution`

Basic task to check if the constraints imposed by all selected semantics are satisfiable.
If so, a satisfying distribution is returned as witness. 
Note that such a distribution in many cases is not the unique solution but only one representative from an infinite solution space. 

**Example:** Look for a distribution on the example AF that is min-complete (`MinCmp`) but not justifiable (`Jus`):

    $ cpraa -f AFs/example.tgf --semantics MinCmp --complement_semantics Jus --one_distribution
    Computing one distribution satisfying the following semantics: MinCmp, co-Jus
    Support:
    P(-A,-B, C) = 0.5
    P( A,-B,-C) = 0.5


### Enumerate vertices of convex solution space 
`-CD`, `--corner_distributions`

This task requires linear constraints, as otherwise it is not guaranteed that the solution space is convex.
The distributions (viewed as vectors in n-dimensional space) located at the corners of a convex solution space have the nice property that all solutions can be stated as a convex combination of them.
In case this task yields only a single distribution, the solution is unique.

**Example:** Find the corner distributions for element-wise completeness (`ElmCmp`) in the example AF:

    $ cpraa -f AFs/example.tgf --semantics ElmCmp --corner_distributions
    Computing the corner distributions for the following semantics: ElmCmp
    
    Result 1 of 3:
    Support:
    P(-A,-B,-C) = 1
    
    Result 2 of 3:
    Support:
    P(-A, B,-C) = 1
    
    Result 3 of 3:
    Support:
    P( A,-B, C) = 1

As expected, the resulting distributions are the Dirac distributions of the assignments corresponding to all three complete assignments of the example AF. 


### Optimize marginal probabilities

`-MIN`, `--minimize_probability`, or `-MAX`, `--maximize_probability`

This task requires linear constraints and one or more arguments from the AF (passed with `--arguments` or `-a`).
If the constraints are satisfiable, the resulting distribution minimises (or respectively maximises) the marginal probability of the given argument, or, if multiple arguments are given, the probability of any argument holding.

**Example:** (TODO)

    $ cpraa -f AFs\example.tgf --semantics PrCmp -a B -MAX
    Computing optimal distribution maximizing the probability of argument B while satisfying the following semantics: PrCmp
    Support:
    P(-A, B,-C) = 1


### Acceptance checking for arguments

`-CA`, `--credulous_acceptance`

`-SA`, `--skeptical_acceptance`

`-CAA`, `--credulous_acceptance_all`

`-SAA`, `--skeptical_acceptance_all`

(TODO)


### Generate labelings

`-OL`, `--one_labeling`

`-AL`, `--all_labelings`

(TODO)


## Further options

`-smt`, `--smt_file`

`-b`, `--backend_solver`

`-t`, `--time`

`-o`, `--distribution_output_format`

`-p`, `--output_precision`

`-dc`, `--display_constraints`


(TODO)
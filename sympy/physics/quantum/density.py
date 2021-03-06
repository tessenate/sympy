from sympy import Tuple, Add, Matrix, log, expand
from sympy.printing.pretty.stringpict import prettyForm
from sympy.physics.quantum.dagger import Dagger
from sympy.physics.quantum.operator import HermitianOperator, OuterProduct
from sympy.physics.quantum.represent import represent
from sympy.physics.quantum.state import KetBase
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.qapply import qapply
from matrixutils import numpy_ndarray, scipy_sparse_matrix, to_numpy


class Density(HermitianOperator):
    """Density operator for representing mixed states.

    TODO: Density operator support for Qubits

    Parameters
    ==========

    values : tuples/lists
    Each tuple/list should be of form (state, prob) or [state,prob]

    Examples
    =========

    Create a density operator with 2 states represented by Kets.

    >>> from sympy.physics.quantum.state import Ket
    >>> from sympy.physics.quantum.density import Density
    >>> d = Density([Ket(0), 0.5], [Ket(1),0.5])
    >>> d
    'Density'((|0>, 0.5),(|1>, 0.5))

    """

    @classmethod
    def _eval_args(cls, args):
        # call this to qsympify the args
        args = super(Density, cls)._eval_args(args)

        for arg in args:
            # Check if arg is a tuple
            if not (isinstance(arg, Tuple) and
                     len(arg) == 2 ):
                raise ValueError("Each argument should be of form [state,prob]"
                                 " or ( state, prob )")

        return args

    def states(self):
        """Return list of all states.

        Examples
        =========

        >>> from sympy.physics.quantum.state import Ket
        >>> from sympy.physics.quantum.density import Density
        >>> d = Density([Ket(0), 0.5], [Ket(1),0.5])
        >>> d.states()
        (|0>, |1>)

        """
        return Tuple(*[arg[0] for arg in self.args])

    def probs(self):
        """Return list of all probabilities.

        Examples
        =========

        >>> from sympy.physics.quantum.state import Ket
        >>> from sympy.physics.quantum.density import Density
        >>> d = Density([Ket(0), 0.5], [Ket(1),0.5])
        >>> d.probs()
        (0.5, 0.5)

        """
        return Tuple(*[arg[1] for arg in self.args])

    def get_state(self, index):
        """Return specfic state by index.

        Parameters
        ==========

        index : index of state to be returned

        Examples
        =========

        >>> from sympy.physics.quantum.state import Ket
        >>> from sympy.physics.quantum.density import Density
        >>> d = Density([Ket(0), 0.5], [Ket(1),0.5])
        >>> d.states()[1]
        |1>

        """
        state = self.args[index][0]
        return state

    def get_prob(self, index):
        """Return probability of specific state by index.

        Parameters
        ===========

        index : index of states whose probability is returned.

        Examples
        =========

        >>> from sympy.physics.quantum.state import Ket
        >>> from sympy.physics.quantum.density import Density
        >>> d = Density([Ket(0), 0.5], [Ket(1),0.5])
        >>> d.probs()[1]
        0.500000000000000

        """
        prob = self.args[index][1]
        return prob

    def apply_op(self, op):
        """op will operate on each individual state.

        Parameters
        ==========

        op : Operator

        Examples
        =========

        >>> from sympy.physics.quantum.state import Ket
        >>> from sympy.physics.quantum.density import Density
        >>> from sympy.physics.quantum.operator import Operator
        >>> A = Operator('A')
        >>> d = Density([Ket(0), 0.5], [Ket(1),0.5])
        >>> d.apply_op(A)
        'Density'((A*|0>, 0.5),(A*|1>, 0.5))

        """
        new_args = [(op*state, prob) for (state, prob) in self.args]
        return Density(*new_args)

    def doit(self, **hints):
        """Expand the density operator into an outer product format.

        Examples
        =========

        >>> from sympy.physics.quantum.state import Ket
        >>> from sympy.physics.quantum.density import Density
        >>> from sympy.physics.quantum.operator import Operator
        >>> A = Operator('A')
        >>> d = Density([Ket(0), 0.5], [Ket(1),0.5])
        >>> d.doit()
        0.5*|0><0| + 0.5*|1><1|

        """
        terms = []
        for (state, prob) in self.args:
            terms.append(prob*(state*Dagger(state)))

        return Add(*terms)

    def _represent(self, **options):
        return represent(self.doit(), **options)

    def _print_operator_name_latex(self, printer, *args):
        return printer._print(r'\rho', *args)

    def _print_operator_name_pretty(self, printer, *args):
        return prettyForm(u"\u03C1")

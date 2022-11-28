import numpy as np
import matplotlib.pyplot as plt
from utility import PolyCurve


def plot_curves(P : PolyCurve, Q : PolyCurve, ax=None, markers=None):
    if ax is None:
        fig, ax_ = plt.subplots(1)
    else:
        ax_ = ax

    ax_.set_title("Curves P and Q")

    # plot P and Q
    P_line = ax_.plot(*P.coords, 'o-', color='blue', linewidth=2)
    Q_line = ax_.plot(*Q.coords, 'o-', color='red', linewidth=2)

    if markers is not None:
        marker_loc = np.array(
            [P.parametric(markers[0])] + [Q.parametric(markers[1])])

        # leash connection
        leash = ax_.plot(marker_loc[:, 0], marker_loc[:, 1], 'o-',
                         markerfacecolor='black', markersize=8, color='orange', linewidth=2)

        marker_dst = np.linalg.norm(marker_loc[0, :]-marker_loc[1, :])

        ax_.legend(('P', 'Q', f'Leash, length={round(marker_dst,2)}'))
    else:
        ax_.legend((P_line, Q_line), ('P', 'Q'))

    if ax is None:
        fig.show()

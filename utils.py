import matplotlib.pyplot as plt; plt.style.use("fivethirtyeight")
from sklearn.metrics import accuracy_score, f1_score, auc, roc_auc_score, roc_curve


def plot_roc(y, probs, verbose=True):
    if len(probs.shape) > 1:
        preds = probs[:,1]
    else:
        preds = probs
    fpr, tpr, threshold = roc_curve(y, preds)
    roc_auc = auc(fpr, tpr)

    if verbose:
        plt.title('Receiver Operating Characteristic')
        plt.plot(fpr, tpr, 'b', label = 'AUC = %0.4f' % roc_auc)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show()
    return roc_auc
    
    
def evaluate(model, x, y, verbose=True):
    probs = model.predict_proba(x)
    y_pred = probs[:, 1] > 0.5
    acc = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    if verbose:
        print("Accuracy: {:.2f}".format(acc * 100))
        print("F-1 score: {:.4f}".format(f1))
    return plot_roc(y, probs, verbose=verbose)



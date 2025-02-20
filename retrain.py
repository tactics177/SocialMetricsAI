from app import train_model


def retrain():
    global model
    model = train_model()
    print("Model retrained successfully.")


if __name__ == "__main__":
    retrain()

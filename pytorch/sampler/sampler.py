import numpy as np
import torch


def balanced_sampler(labels, number_of_samples_per_label_function, replacement):
    class_counts = np.bincount(labels)
    class_weights = [
        (np.float64(1.0) / class_counts[label]) * np.sum(class_counts) / 2
        for label in np.unique(labels)
    ]

    number_of_samples_per_label = number_of_samples_per_label_function(class_counts)
    number_of_samples = int(number_of_samples_per_label * len(class_counts))

    sample_weights = [class_weights[label] for label in labels]
    return torch.utils.data.WeightedRandomSampler(sample_weights, number_of_samples, replacement)

def oversampler(labels):
    return balanced_sampler(labels, number_of_samples_per_label_function=np.max, replacement=True)

def undersampler(labels, replacement=False):
    return balanced_sampler(labels, number_of_samples_per_label_function=np.min, replacement=replacement)


if __name__ == '__main__':
    from torch.utils.data import DataLoader

    dataset = make_dataset()
    labels = get_labels_from_dataset(dataset)

    balanced_dataloader_oversampled = DataLoader(
        dataset,
        sampler=oversampler(labels),
        num_workers=torch.get_num_threads(),
    )

    balanced_dataloader_undersampled = DataLoader(
        dataset,
        sampler=undersampler(labels),
        num_workers=torch.get_num_threads(),
    )

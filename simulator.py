import random
import markovify


STATE_SIZE = 3
MAX_OVERLAP_RATIO = 0.5
MAX_OVERLAP_TOTAL = 10


class User:
    def build_comment(self):
        """
        Builds a comment based on the average length
        """

        comment = ""
        while True:
            # Literally the only case a while loop is useful

            # For each sentence, check how close to the average comment length
            # we are, then use the remaining percentage as the chance of
            # adding another sentence. For example, if we're at 70% of the
            # average comment length, there will be a 30% chance of adding
            # another sentence. We're also adding a fixed 10% on top of that
            # just to increase the length a little, and have some chance of
            # continuing once we're past the average.
            portion_done = len(comment) / float(self.average_message_len)
            continue_chance = 1.0 - portion_done
            continue_chance = max(0, continue_chance)
            continue_chance += 0.1
            if random.random() > continue_chance:
                break

            new_sentence = self.model.make_sentence(
                tries=10000,
                max_overlap_total=MAX_OVERLAP_TOTAL,
                max_overlap_ratio=MAX_OVERLAP_RATIO,
            )
            comment += " " + new_sentence

        comment = comment.strip()

        return comment

    def get_markov(self, messages):
        avg_messages_len = sum(len(c) for c in messages) / float(len(messages))
        self.avg_messages_len = min(250, avg_messages_len)
        self.model = markovify.Text("\n".join(messages), state_size=STATE_SIZE)
        return self.build_comment()

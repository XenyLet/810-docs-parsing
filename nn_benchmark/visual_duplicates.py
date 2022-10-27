from pprint import pprint

class DupFileReader:
    def __init__(self, 
                 file_path, 
                 comment_symbol='#', 
                 cyr_head='кир',
                 lat_head='лат',
                 digit_head='цифр',
                 additional_head='доп',
                 head_split=':'):
        self.comment_symbol = comment_symbol
        self.head_split = head_split
        self.heads={
            cyr_head: 'cyr',
            lat_head: 'lat',
            digit_head: 'dig',
            additional_head: 'add'
        }
        self.priority=['lat', 'cyr', 'dig']

        self.duplicates_tuples = []

        with open(file_path, "rt") as f:
            data = f.readlines()

        self._parse_lines(self._clean_lines(data))



    def _clean_lines(self, file_lines):
        return [
            line.strip() 
            for line in file_lines 
            if line.strip()[0] != self.comment_symbol 
        ]


    def _parse_lines(self, file_lines):
        dupes_data = {
            k: []
            for k in self.heads.values()
        }

        # grab data
        additional_line_data=[]
        for l in file_lines:
            head, data = l.split(self.head_split)
            head_alias = head.strip()
            if head_alias in self.heads:
                head_id = self.heads[head_alias]
            else:
                raise ValueError(f"Unknown head: \"{h}\"")

            if head_id != 'add':
                dupes_data[head_id] = list(data.rstrip())
            else:
                additional_line_data = data.split(',')
            

        # equalize lengths
        max_len = len(max(dupes_data.values(), key=len))
        for head_id, d in dupes_data.items():
            diff = max_len - len(d)
            dupes_data[head_id] += [' ']*diff


        #make pairs
        pair_order = self.priority
        pairs = list(zip(
                *[
                    dupes_data[k] 
                    for k in pair_order
                ]
            ))
        # add additional pairs
        pairs.extend(
            [tuple(p) for p in additional_line_data]
            )


        self.duplicates_tuples = pairs
        # pprint(self.duplicates_tuples)


    def _find_duplicates_tuple(self, ch):
        for dup in self.duplicates_tuples:
            if ch in dup:
                return dup
        return None


    def _deduplicate(self, ch):
        dup = self._find_duplicates_tuple(ch)
        if dup:
            return dup[0] # symbol with maximum priority
        return ch

    def filter_str(self, str_to_deduplicate):
        dup_map = {
            old_ch: self._deduplicate(old_ch)
            for old_ch in set(str_to_deduplicate)
        }
        res = ''.join([
                dup_map[old_ch] 
                for old_ch 
                in str_to_deduplicate
            ])
        return res

    def get_similar(self, ch):
        dup = self._find_duplicates_tuple(ch)
        if dup:
            return ''.join(dup).strip()
        return None


if __name__ == '__main__':
    import sys

    if sys.argv[1] == 'dedup':
        fname = sys.argv[2]
        tgt_str = sys.argv[3]

        reader = DupFileReader(fname)
        print(reader.filter_str(tgt_str))

    elif sys.argv[1] == 'similar':
        fname = sys.argv[2]
        tgt_char = sys.argv[3]

        reader = DupFileReader(fname)
        similars = reader.get_similar(tgt_char)
        if similars:
            print(''.join(similars))









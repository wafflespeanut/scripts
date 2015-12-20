import os

path = os.path.expanduser('~/Desktop/Desktop/Dropbox/Recordings/')
in_path, out_path = path + 'Calls (Raw)', path + 'Calls'

if __name__ == '__main__':      # one-time sorting of recordings
    nums = {}
    for record in os.listdir(in_path):
        name, ext = record.split('.')
        try:
            year, month, day, hour, mins, contact, what = name.split('_')
        except ValueError:
            print '%r does not fit the format!' % record
            continue
        contact = contact[2:] if contact.startswith('91') and len(contact) == 12 else contact
        new_name = '{}-{}-{} ({}-{}) {}.{}' \
                   .format(year, month, day, hour, mins, what.title(), ext)
        if nums.has_key(contact):
            nums[contact].append((record, new_name))
        else:
            nums[contact] = [(record, new_name)]

    for (contact, records) in nums.iteritems():
        folder_name = os.path.join(out_path, contact)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        for old_name, new_name in records:
            old_path = os.path.join(in_path, old_name)
            new_path = os.path.join(folder_name, new_name)
            if os.path.exists(new_path):
                print '%r already exists!' % new_path
                continue
            os.rename(old_path, new_path)

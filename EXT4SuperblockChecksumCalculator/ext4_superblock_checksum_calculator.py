'''
crc32c package from pip (https://pypi.org/project/crc32c/) copyright:

ICRAR - International Centre for Radio Astronomy Research
(c) UWA - The University of Western Australia, 2017
Copyright by UWA (in the framework of the ICRAR)
'''

# It's completely USELESS since i have no idea how they are calculating it
# in ext4 superblock... BUT

# This script can calculate crc32c of your superblock in different ways:
# *Whole raw superblock (always some 0xffffffff thing)
# *Superblock without checksum (as it meant in documentation here: https://ext4.wiki.kernel.org/index.php/Ext4_Disk_Layout#The_Super_Block)
# *Fields-reversed superblock (see rev function)
# *Fully-reversed superblock (makes no sense ehhh)
# *Only little-endian variables reversed superblock (see "if True" or "if False"
# after the variables reading)
# *You may add zero-checksum field or delete it (see code after "if" field from
# previous option)
# *There is also a CSV parser for you to make list of offsets, lengths and
# variable names from the documentation, see parseCSV() function!

import crc32c

# my device with ext4
DEVICE="/dev/sda7"
# my prepared file with csv
CSV_PATH="superblock_csv_example.csv"


def readSuperblockInfo ( pathToDevice ):
    file=open(pathToDevice,"r")
    # Offset of a superblock
    sb_offset=0x400
    file.seek(sb_offset)
    bytes=file.read(1024)
    file.close()
    print("ORIGINAL SUPERBLOCK:")
    print(bytes.encode('hex'))
    print("")


    # 0x3FC - offset to checksum
    bytes_nocs=bytes[0:0x3FC]
    fully_reversed_sb=rev(bytes_nocs)
    print("FULLY-REVERSED SUPERBLOCK WITHOUT CHECKSUM:")
    print(fully_reversed_sb.encode('hex'))
    print("")
    # Actually, this all must be readed from parser but i wrote it after all
    # variables was done...

    # all fields of the superblock separately reversed
    # to undo reverse go to rev function and comment it
    s_inodes_count=rev(bytes[0x0:0x0+4])
    s_blocks_count_lo=rev(bytes[0x4:0x4+4])
    s_r_blocks_count_lo=rev(bytes[0x8:0x8+4])
    s_free_blocks_count_lo=rev(bytes[0xC:0xC+4])
    s_free_inodes_count=rev(bytes[0x10:0x10+4])
    s_first_data_block=rev(bytes[0x14:0x14+4])
    s_log_block_size=rev(bytes[0x18:0x18+4])
    s_log_cluster_size=rev(bytes[0x1C:0x1C+4])
    s_blocks_per_group=rev(bytes[0x20:0x20+4])
    s_clusters_per_group=rev(bytes[0x24:0x24+4])
    s_inodes_per_group=rev(bytes[0x28:0x28+4])
    s_mtime=rev(bytes[0x2C:0x2C+4])
    s_wtime=rev(bytes[0x30:0x30+4])
    s_mnt_count=rev(bytes[0x34:0x34+2])
    s_max_mnt_count=rev(bytes[0x36:0x36+2])
    s_magic=rev(bytes[0x38:0x38+2])
    s_state=rev(bytes[0x3A:0x3A+2])
    s_errors=rev(bytes[0x3C:0x3C+2])
    s_minor_rev_level=rev(bytes[0x3E:0x3E+2])
    s_lastcheck=rev(bytes[0x40:0x40+4])
    s_checkinterval=rev(bytes[0x44:0x44+4])
    s_creator_os=rev(bytes[0x48:0x48+4])
    s_rev_level=rev(bytes[0x4C:0x4C+4])
    s_def_resuid=rev(bytes[0x50:0x50+2])
    s_def_resgid=rev(bytes[0x52:0x52+2])

    ##
    # EXT4_DYNAMIC_REV superblock only fields
    ##

    s_first_ino=rev(bytes[0x54:0x54+4])
    s_inode_size=rev(bytes[0x58:0x58+2])
    s_block_group_nr=rev(bytes[0x5A:0x5A+2])
    s_feature_compat=rev(bytes[0x5C:0x5C+4])
    s_feature_incompat=rev(bytes[0x60:0x60+4])
    s_feature_ro_compat=rev(bytes[0x64:0x64+4])

    s_uuid=bytes[0x68:0x68+16] # u8 [16]
    s_volume_name=bytes[0x78:0x78+16] # char [16]
    s_last_mounted=bytes[0x88:0x88+64] # char [64]

    s_algorithm_usage_bitmap=rev(bytes[0xC8:0xC8+4])

    ##
    # Performance hints. Directory preallocation should only happen if
    # EXT_4_FEATURE_CIMPAT_DIR_PREALLOC flag is on
    ##

    s_prealloc_blocks=bytes[0xCC:0xCC+1] # u8
    s_prealloc_dir_blocks=bytes[0xCD:0xCD+1] # u8

    s_reserved_gdt_blocks=rev(bytes[0xCE:0xCE+2])

    ##
    # Journaling support vaild if EXT_4_FEATURE_CIMPAT_HAS_JOURNAL set
    ##

    s_journal_uuid=bytes[0xD0:0xD0+1*16] # u8[16]

    s_journal_inum=rev(bytes[0xE0:0xE0+4])
    s_journal_dev=rev(bytes[0xE4:0xE4+4])
    s_last_orphan=rev(bytes[0xE8:0xE8+4])
    s_hash_seed=rev(bytes[0xEC:0xEC+4*4]) # le32[4]

    s_def_hash_version=bytes[0xFC:0xFC+1] # u8
    s_jnl_backup_type=bytes[0xFD:0xFD+1] # u8

    s_desc_size=rev(bytes[0xFE:0xFE+2])
    s_default_mount_opts=rev(bytes[0x100:0x100+4])
    s_first_meta_bg=rev(bytes[0x104:0x104+4])
    s_mkfs_time=rev(bytes[0x108:0x108+4])
    s_jnl_blocks=rev(bytes[0x10C:0x10C+4*17]) # le32[17]

    ##
    # 64bit support valid if EXT_4_FEATURE_CIMPAT_64BIT
    ##

    s_blocks_count_hi = rev(bytes[0x150:0x150+4])
    s_r_blocks_count_hi = rev(bytes[0x154:0x154+4])
    s_free_blocks_count_hi = rev(bytes[0x158:0x158+4])
    s_min_extra_isize = rev(bytes[0x15C:0x15C+2])
    s_want_extra_isize = rev(bytes[0x15E:0x15E+2])
    s_flags=rev(bytes[0x160:0x160+4])
    s_raid_stride=rev(bytes[0x164:0x164+2])
    s_mmp_interval=rev(bytes[0x166:0x166+2])
    s_mmp_block=rev(bytes[0x168:0x168+8])
    s_raid_stripe_width=rev(bytes[0x170:0x170+4])

    s_log_groups_per_flex=bytes[0x174:0x174+1] #u8
    s_checksum_type=bytes[0x175:0x175+1] # u8, the only valid value is 1 - crc32c

    s_reserved_pad=rev(bytes[0x176:0x176+2])
    s_kbytes_written=rev(bytes[0x178:0x178+8])
    s_snapshot_inum=rev(bytes[0x180:0x180+4])

    s_snapshot_id=rev(bytes[0x184:0x184+4])
    s_snapshot_r_blocks_count=rev(bytes[0x188:0x188+8])
    s_snapshot_list=rev(bytes[0x190:0x190+4])

    s_error_count=rev(bytes[0x194:0x194+4])
    s_first_error_time=rev(bytes[0x198:0x198+4])
    s_first_error_ino=rev(bytes[0x19C:0x19C+4])
    s_first_error_block=rev(bytes[0x1A0:0x1A0+8])

    s_first_error_func=bytes[0x1A8:0x1A8+1*32] # u8[32]

    s_first_error_line=rev(bytes[0x1C8:0x1C8+4])
    s_last_error_time=rev(bytes[0x1CC:0x1CC+4])
    s_last_error_ino=rev(bytes[0x1D0:0x1D0+4])
    s_last_error_line=rev(bytes[0x1D4:0x1D4+4])
    s_last_error_block=rev(bytes[0x1D8:0x1D8+8])

    s_last_error_func=bytes[0x1E0:0x1E0+1*32] # u8[32]
    s_mount_opts=bytes[0x200:0x200+1*64] # u8[64]

    s_usr_quota_inum=rev(bytes[0x240:0x240+4])
    s_grp_quota_inum=rev(bytes[0x244:0x244+4])

    s_overhead_blocks=rev(bytes[0x248:0x248+4])
    s_backup_bgs=rev(bytes[0x24C:0x24C+4*2]) #le32[2]

    s_encrypt_algos=bytes[0x254:0x254+1*4] #u8[4]
    s_encrypt_pw_salt=bytes[0x258:0x258+1*16] #u8[16]

    s_lpf_ino=rev(bytes[0x268:0x268+4])
    s_prj_quota_inum=rev(bytes[0x26C:0x26C+4])
    s_checksum_seed=rev(bytes[0x270:0x270+4])
    s_reserved=rev(bytes[0x274:0x274+4*98]) #le32[98]
    s_checksum=rev(bytes[0x3FC:0x3FC+4])

    # only for console output
    s_cs=s_checksum

    # reverse or no reverse u8 and chars:
    if True:
        s_uuid=rev(bytes[0x68:0x68+16]) # u8 [16]
        s_volume_name=rev(bytes[0x78:0x78+16]) # char [16]
        s_last_mounted=rev(bytes[0x88:0x88+64]) # char [64]
        s_prealloc_blocks=rev(bytes[0xCC:0xCC+1]) # u8
        s_prealloc_dir_blocks=rev(bytes[0xCD:0xCD+1]) # u8
        s_journal_uuid=rev(bytes[0xD0:0xD0+1*16]) # u8[16]
        s_def_hash_version=rev(bytes[0xFC:0xFC+1]) # u8
        s_jnl_backup_type=rev(bytes[0xFD:0xFD+1]) # u8
        s_log_groups_per_flex=rev(bytes[0x174:0x174+1]) #u8
        s_checksum_type=rev(bytes[0x175:0x175+1]) # u8, the only valid value is 1 - crc32c
        s_first_error_func=rev(bytes[0x1A8:0x1A8+1*32]) # u8[32]
        s_last_error_func=rev(bytes[0x1E0:0x1E0+1*32]) # u8[32]
        s_mount_opts=rev(bytes[0x200:0x200+1*64]) # u8[64]
        s_encrypt_algos=rev(bytes[0x254:0x254+1*4]) #u8[4]
        s_encrypt_pw_salt=rev(bytes[0x258:0x258+1*16]) #u8[16]


    # fill checksum with zeroes
    #s_checksum="\x00\x00\x00\x00"

    big_array=[ s_inodes_count,s_blocks_count_lo,s_r_blocks_count_lo,s_free_blocks_count_lo,s_free_inodes_count,s_first_data_block,s_log_block_size,s_log_cluster_size,s_blocks_per_group,s_clusters_per_group,s_inodes_per_group,s_mtime,s_wtime,s_mnt_count,s_max_mnt_count,s_magic,s_state,s_errors,s_minor_rev_level,s_lastcheck,s_checkinterval,s_creator_os,s_rev_level,s_def_resuid,s_def_resgid,s_first_ino,s_inode_size,s_block_group_nr,s_feature_compat,s_feature_incompat,s_feature_ro_compat,s_uuid,s_volume_name,s_last_mounted,s_algorithm_usage_bitmap,s_prealloc_blocks,s_prealloc_dir_blocks,s_reserved_gdt_blocks,s_journal_uuid,s_journal_inum,s_journal_dev,s_last_orphan,s_hash_seed,s_def_hash_version,s_jnl_backup_type,s_desc_size,s_default_mount_opts,s_first_meta_bg,s_mkfs_time,s_jnl_blocks,s_blocks_count_hi,s_r_blocks_count_hi,s_free_blocks_count_hi,s_min_extra_isize,s_want_extra_isize,s_flags,s_raid_stride,s_mmp_interval,s_mmp_block,s_raid_stripe_width,s_log_groups_per_flex,s_checksum_type,s_reserved_pad,s_kbytes_written,s_snapshot_inum,s_snapshot_id,s_snapshot_r_blocks_count,s_snapshot_list,s_error_count,s_first_error_time,s_first_error_ino,s_first_error_block,s_first_error_func,s_first_error_line,s_last_error_time,s_last_error_ino,s_last_error_line,s_last_error_block,s_last_error_func,s_mount_opts,s_usr_quota_inum,s_grp_quota_inum,s_overhead_blocks,s_backup_bgs,s_encrypt_algos,s_encrypt_pw_salt,s_lpf_ino,s_prj_quota_inum,s_checksum_seed,s_reserved,s_checksum]
    big_array.pop(90) # delete checksum
    #print(big_array)

    # reversed superblock
    reversed_fields_sb=""
    for s in big_array:
        reversed_fields_sb=reversed_fields_sb+s

    #print(bytes==reversed_fields_sb)
    print("FIELDS-REVERSED SUPERBLOCK:")
    print(reversed_fields_sb.encode('hex'))
    print("")
    #print(len(big_array))
    #print(len(reversed_fields_sb))
    #for b in big_array:
        #print(b.encode('hex'))


    #######
    print("")
    print("ORIGINAL CHECKSUM (not calculated!): 0x"+rev(s_cs).encode('hex'))
    print("")
    print("CALCULATED WHOLE SUPERBLOCK: "+hex(crc32c.crc32(bytes)))
    ## WARNING WARNING WARNING
    # basically it has no sense to crc32c something from encode() function
    # since it's just string which look like hex
    # the real raw bytes stored in pure strings without encoding
    ##
    print(hex(crc32c.crc32(bytes.encode('hex'))))

    print("CALCULATED SUPERBLOCK WITHOUT CHECKSUM: "+hex(crc32c.crc32(bytes_nocs)))
    print(hex(crc32c.crc32(bytes_nocs.encode('hex'))))

    print("CALCULATED FULLY-REVERSED SUPERBLOCK WITHOUT CHECKSUM: "+hex(crc32c.crc32(fully_reversed_sb)))
    print(hex(crc32c.crc32(fully_reversed_sb.encode('hex'))))

    print("CALCULATED FIELDS-REVERSED SUPERBLOCK: "+hex(crc32c.crc32(reversed_fields_sb)))
    print(hex(crc32c.crc32(reversed_fields_sb.encode('hex'))))


# simple arrays reverser
def rev ( array ):
    # add comment here to BLOCK reversing
    array=array[::-1]
    return array


# you MUST to prepare your csv first:
# for example, be sure to delete all one-row hints from it
# do not insert in it DESCRIPTIONS, only three field: offset, length and name!
def parseCSV ( path ):
    offsets = [ ]
    lengths = [ ]
    names = [ ]
    # this is specification of superblock from https://ext4.wiki.kernel.org/index.php/Ext4_Disk_Layout#The_Super_Block
    f=open(path,"r")
    i=0
    for line in f:
        i=i+1
        p=0
        offset=""
        length=""
        name=""
        for c in line:
            if c=='\n': break
            if c==',':
                p=p+1
                continue
            if p==0: offset=offset+c
            if p==1: length=length+c
            if p==2: name=name+c

        #offsets.append(offset.encode('hex'))
        offsets.append(offset)
        if length=="__le64": length=8
        if length=="__le32": length=4
        if length=="__le16": length=2
        if length=="__u8": length=1
        if length=="char": length=1

        new_name=""
        mult_length=""
        if '[' in name:
            isNum=False
            for c in name:
                if c=='[':
                    isNum=True
                    continue
                if c==']': break
                if isNum:
                    mult_length=mult_length+c
                    continue
                new_name=new_name+c
            name=new_name
            length=length*int(mult_length)
        lengths.append(length)
        names.append(name)
    f.close()

    # this will give you a list of names to place it in some array such as big_array
    '''
    string_variables=""
    for s in names:
        string_variables=string_variables+s+","
    print(string_variables)
    '''

    # this must give out the size of your block from documentation
    sum=0
    for l in lengths:
        sum=sum+l
    print("PARSED LENGTH: "+str(sum))
    print("")




parseCSV(CSV_PATH)
readSuperblockInfo(DEVICE)

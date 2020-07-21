from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

main_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(
            text=('➕ Add new photos'),
        )],
        [KeyboardButton(
            text=('📃 Photo list'),
        )]
    ], resize_keyboard=True, one_time_keyboard=True
)

text_back_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(
            text=('🔙 Back'),
        )]
    ], resize_keyboard=True, one_time_keyboard=True
)

line_back_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
        text='🔙 Back',
        callback_data='back_to_photo')]
    ]
)

accept_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
        text='✅ Yes',
        callback_data='accept')
        ],
        [InlineKeyboardButton(
        text='❎ No',
        callback_data='decline')
        ]
    ], row_width=2
)

post_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='✏️ Update Author',
            callback_data='update_author'
        )],
        [InlineKeyboardButton(
            text='🗑 Delete',
            callback_data='delete_photo'
        )],
        [InlineKeyboardButton(
            text='🔙 Back',
            callback_data='back_to_list'
        )]
    ]
)
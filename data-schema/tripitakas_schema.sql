-- 如是经data_rssutra
CREATE TABLE IF NOT EXISTS data_rssutra (
  id BIGSERIAL PRIMARY KEY,
  rssutra_code varchar(32) DEFAULT NULL, -- '编码。如RS_1'
  sutra_no int DEFAULT NULL, -- '经号'
  sutra_variant_no int DEFAULT NULL, -- '别本号'
  name varchar(128) DEFAULT NULL, -- '经名'
  total_reels int DEFAULT NULL, -- '应存卷数'
  cur_reels int DEFAULT NULL, -- '现存卷数'
  author varchar(128) DEFAULT NULL, -- '作译者'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);

-- 如是卷data_rsreel
CREATE TABLE IF NOT EXISTS data_rsreel (
  id BIGSERIAL PRIMARY KEY,
  rsreel_code varchar(32) DEFAULT NULL, -- '编码。如RS_1_1'
  base_reel varchar(32) DEFAULT NULL, -- '底本编码。如YB_1_1'
  reel_no int DEFAULT NULL, -- '卷序号'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);

-- 实体藏data_tripitaka
CREATE TABLE IF NOT EXISTS data_tripitaka (
  id BIGSERIAL PRIMARY KEY,
  tripitaka_code varchar(32) DEFAULT NULL, -- '编码。如YB/SX'
  name varchar(32) DEFAULT NULL, -- '名称。如永乐北藏/思溪藏'
  shortname varchar(8) DEFAULT NULL, -- '简称。如永北/思溪'
  store_mode smallint DEFAULT NULL, -- '存储结构。1表示藏册页，2表示藏函册页，3表示藏经卷页'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);


-- 实体函data_envelope
CREATE TABLE IF NOT EXISTS data_envelope (
  id BIGSERIAL PRIMARY KEY,
  envelope_code varchar(32) DEFAULT NULL, -- '编码。如SX_2'
  env_no int DEFAULT NULL, -- '函序号'
  total_volumes int DEFAULT NULL, -- '应存册数'
  cur_volumes int DEFAULT NULL, -- '现存册数'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);

-- 实体册data_volume
CREATE TABLE IF NOT EXISTS data_volume (
  id BIGSERIAL PRIMARY KEY,
  volume_code varchar(32) DEFAULT NULL, -- '编码。如YB_1/SX_2_1'
  env_no int DEFAULT NULL, -- '函序号'
  vol_no int DEFAULT NULL, -- '册序号'
  cover_pages int DEFAULT NULL, -- '封面页数'
  back_pages int DEFAULT NULL, -- '封底页数'
  txt_pages int DEFAULT NULL, -- '应存正文页数'
  cur_txt_pages int DEFAULT NULL, -- '现存正文页数'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);

-- 实体经data_sutra
CREATE TABLE IF NOT EXISTS data_sutra (
  id BIGSERIAL PRIMARY KEY,
  sutra_code varchar(32) DEFAULT NULL, -- '编码。如YB_1/YB_123b1，b1表示别本号为1'
  sutra_no int DEFAULT NULL, -- '经序号'
  sutra_variant_no int DEFAULT NULL, -- '别本号'
  name varchar(128) DEFAULT NULL, -- '经名'
  total_reels int DEFAULT NULL, -- '应存卷数'
  cur_reels int DEFAULT NULL, -- '现存卷数'
  author varchar(128) DEFAULT NULL, -- '作译者'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);


-- 实体卷data_reel
CREATE TABLE IF NOT EXISTS data_reel (
  id BIGSERIAL PRIMARY KEY,
  reel_code varchar(32) DEFAULT NULL, -- '编码。如YB_1_1'
  sutra_no int DEFAULT NULL, -- '经序号'
  reel_no int DEFAULT NULL, -- '卷序号'
  start_vol int DEFAULT NULL, -- '起始册'
  start_vol_page int DEFAULT NULL, -- '起始页'
  end_vol int DEFAULT NULL, -- '终止册'
  end_vol_page int DEFAULT NULL, -- '终止页'
  txt_pages int DEFAULT NULL, -- '正文页数'
  has_inner smallint DEFAULT NULL, -- '卷内结构。值为有或者无，如果实体卷卷内还有序跋等，则为有；否则为无。'
  simple_txt text DEFAULT NULL, -- '简单文本'
  mark_txt varchar(128) DEFAULT NULL, -- '标注文本'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);

-- 实体卷卷内结构data_inner_reel
CREATE TABLE IF NOT EXISTS data_inner_reel (
  id BIGSERIAL PRIMARY KEY,
  reel_code varchar(32) DEFAULT NULL, -- '编码。如YB_1_1'
  typ smallint DEFAULT NULL, -- '卷内类型。如序、正文、跋'
  inner_no smallint DEFAULT NULL, -- '卷内编号'
  name varchar(128) DEFAULT NULL, -- '名称'
  start_vol int DEFAULT NULL, -- '起始册'
  start_vol_page int DEFAULT NULL, -- '起始页'
  end_vol int DEFAULT NULL, -- '终止册'
  end_vol_page int DEFAULT NULL, -- '终止页'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);

-- 实体页data_page
CREATE TABLE IF NOT EXISTS data_page (
  id BIGSERIAL PRIMARY KEY,
  typ smallint DEFAULT NULL, -- '类型。0目录、1经文'
  page_code varchar(32) DEFAULT NULL, -- '存储编码，如YB_1_1'
  logic_code varchar(128) DEFAULT NULL, -- '页面编码，如GL_1_1_1'
  is_existed smallint DEFAULT NULL, -- '图片是否存在'
  reel_no int DEFAULT NULL, -- '卷序号'
  reel_page_no int DEFAULT NULL, -- '卷内页序号'
  env_no int DEFAULT NULL, -- '函序号'
  vol_no int DEFAULT NULL, -- '册序号'
  vol_page_no int DEFAULT NULL, -- '册内页序号'
  block_cut_status varchar(128) DEFAULT NULL, -- '栏坐标状态。未就位，已OCR，已审定'
  column_cut_status varchar(1024) DEFAULT NULL, -- '列坐标状态。未就位，已OCR，已审定'
  char_cut_status text DEFAULT NULL, -- '字坐标状态。未就位，已OCR，已审定'
  txt_status text DEFAULT NULL, -- '文字状态。未就位，已OCR，已审定'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);

-- 实体列data_column
CREATE TABLE IF NOT EXISTS data_column (
  id BIGSERIAL PRIMARY KEY,
  page_code varchar(32) DEFAULT NULL, -- '存储编码。如YB_1_1'
  block_no smallint DEFAULT NULL, -- '栏序号'
  column_no smallint DEFAULT NULL, -- '列序号'
  image_status varchar(256) DEFAULT NULL, -- '图片状态。未就位，已就位'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);

-- 实体字data_char
CREATE TABLE IF NOT EXISTS data_char (
  id BIGSERIAL PRIMARY KEY,
  page_code varchar(32) DEFAULT NULL, -- '存储编码。如YB_1_1'
  block_no smallint DEFAULT NULL, -- '栏序号'
  column_no smallint DEFAULT NULL, -- '列序号'
  char_no smallint DEFAULT NULL, -- '字序号'
  txt varchar(8) DEFAULT NULL, -- '文字'
  txt_confidence float DEFAULT NULL, -- '文字置信度'
  cut_confidence float DEFAULT NULL, -- '切分置信度'
  image_status varchar(256) DEFAULT NULL, -- '图片状态。未就位，已就位'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  updated_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  updated_at int DEFAULT NULL
);





-- 切分校对状态cut_status
CREATE TABLE IF NOT EXISTS cut_status (
  id BIGSERIAL PRIMARY KEY,
  page_code varchar(32) DEFAULT NULL, -- '页编码'
  block_cut_initial_status smallint DEFAULT NULL, -- '切栏初校状态'
  block_cut_confirm_status smallint DEFAULT NULL, -- '切栏审定状态'
  col_cut_initial_status smallint DEFAULT NULL, -- '切列初校状态'
  col_cut_confirm_status smallint DEFAULT NULL, -- '切列审定状态'
  char_cut_initial_status smallint DEFAULT NULL, -- '切字初校状态'
  char_cut_confirm_status smallint DEFAULT NULL, -- '切字审定状态'
  remark varchar(128) DEFAULT NULL -- '备注'
);

-- 切分校对任务cut_task
CREATE TABLE IF NOT EXISTS cut_task (
  id BIGSERIAL PRIMARY KEY,
  page_code varchar(32) DEFAULT NULL, -- '页编码'
  typ smallint DEFAULT NULL, -- '1表示切字，2表示切列，3表示切栏'
  stage smallint DEFAULT NULL, -- '1表示初校，2表示审定'
  status smallint DEFAULT NULL, -- '状态：未就位，已就位未发布，已发布未领取，进行中，已退回，已完成'
  priority smallint DEFAULT NULL, -- '优先级'
  input text DEFAULT NULL, -- '切分输入'
  result text DEFAULT NULL, -- '切分结果'
  return_reason varchar(128) DEFAULT NULL, -- '退回理由'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  executed_by int DEFAULT NULL,
  picked_at int DEFAULT NULL,
  finished_at int DEFAULT NULL
);


-- 文字校对状态proofread_status
CREATE TABLE IF NOT EXISTS proofread_status (
  id BIGSERIAL PRIMARY KEY,
  page_code varchar(32) DEFAULT NULL, -- '页编码'
  is_data_ready smallint DEFAULT NULL, -- '校对数据是否就位'
  initial_1st_status smallint DEFAULT NULL, -- '校一状态'
  initial_2nd_status smallint DEFAULT NULL, -- '校二状态'
  initial_3rd_status smallint DEFAULT NULL, -- '校三状态'
  initial_4th_status smallint DEFAULT NULL, -- '校四状态'
  confirm_status smallint DEFAULT NULL, -- '审定状态'
  remark varchar(128) DEFAULT NULL -- '备注'
);

-- 文字校对任务proofread_task
CREATE TABLE IF NOT EXISTS proofread_task (
  id BIGSERIAL PRIMARY KEY,
  page_code varchar(32) DEFAULT NULL, -- '页编码'
  stage smallint DEFAULT NULL, -- '1表示初校，2表示审定'
  initial_task_no smallint DEFAULT NULL, -- '1表示初校校一，2表示初校校二，3表示初校校三，4表示初校校四'
  status smallint DEFAULT NULL, -- '状态：未就位，已就位未发布，已发布未领取，进行中，已退回，已完成'
  priority smallint DEFAULT NULL, -- '优先级'
  compare_src varchar(8) DEFAULT NULL, -- '比对本来源：CBETA/GL'
  compare_txt text DEFAULT NULL, -- '比对本文本'
  result_text text DEFAULT NULL, -- '比对结果'
  doubts text DEFAULT NULL, -- '存疑结果'
  return_reason varchar(128) DEFAULT NULL, -- '退回理由'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  executed_by int DEFAULT NULL,
  picked_at int DEFAULT NULL,
  finished_at int DEFAULT NULL
);

-- 文字校对难字proofread_difficultytask
CREATE TABLE IF NOT EXISTS proofread_difficultytask (
  id BIGSERIAL PRIMARY KEY,
  proofread_task_id int DEFAULT NULL, -- '切分校对任务外键'
  page_code varchar(32) DEFAULT NULL, -- '页编码'
  status smallint DEFAULT NULL, -- '状态：0表示未处理，1表示已处理'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  executed_by int DEFAULT NULL,
  picked_at int DEFAULT NULL,
  finished_at int DEFAULT NULL
);

-- 数据标注任务
CREATE TABLE IF NOT EXISTS data_label (
  id BIGSERIAL PRIMARY KEY,
  title varchar(32) DEFAULT NULL, -- '任务名称'
  typ smallint DEFAULT NULL, -- '任务类型：1表示切字校对，2表示切列校对，3表示切框校对，4表示文字校对'
  page_codes text DEFAULT NULL, -- '页编码'
  remark varchar(128) DEFAULT NULL, -- '备注'
  created_by int DEFAULT NULL,
  created_at int DEFAULT NULL,
  finished_at int DEFAULT NULL
);